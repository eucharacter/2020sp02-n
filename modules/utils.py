import os
import uuid
import json

from modules import faceDetect
from modules import tts


def dataURL_to_faces(token, dataURL):
    """根据摄像头照片dataURL获取识别数据，数组的每个元素对应一张脸。
    """
    image64 = faceDetect.dataURL_to_image64(dataURL)

    print(image64[:10])

    result = faceDetect.detect(token, image64)

    # TODO 可以判断一下有没有人脸，再进行下一步操作

    print(result)
    
    face_list = result['face_list']

    return face_list

def picfile_to_faces(token, picfile):
    """根据图片文件流获取识别数据，数组的每个元素对应一张脸。
    """
    image64 = faceDetect.picfile_to_image64(picfile)

    result = faceDetect.detect(token, image64)



    face_list = result['face_list']

    return face_list

def faces_to_display_dicts(faces):
    """给一个数组，每个元素是一张脸的json信息，输出的数组 每个元素是 前端要显示的文本字典

        Args:
            face: json字典，形如：
                {
                'face_token': 'bc3b6b1b097c02a074ffe51600f05a5d',
                'location': {'left': 149.72, 'top': 203.17, 'width': 195, 'height': 173, 'rotation': -4},
                'face_probability': 1,
                'angle': {'yaw': -3.85, 'pitch': 23.26, 'roll': -5.66},
                'age': 26,
                'beauty': 86.31,
                'expression': {'type': 'none', 'probability': 1},
                'gender': {'type': 'male', 'probability': 1},
                'glasses': {'type': 'none', 'probability': 1}
                }
                
        输出数组中每个字典形如：
            {
            'age':int
            'beauty':float
            'expression':'无（微笑，大小）'
            'gender':'男（女）'
            'glasses':'没有戴眼镜（戴了普通眼镜，戴了墨镜）'
            }
        """
    
    display_dicts = []
    
    for face in faces:
        if face['expression']['type']=='none':
            expression = '无'
        elif face['expression']['type']=='smile':
            expression = '微笑'
        else:
            expression = '大笑'

        if face['gender']['type']=='male':
            gender = '男'
        else:
            gender = '女'

        if face['glasses']['type']=='none':
            glasses = '没有戴眼镜'
        elif face['glasses']['type']=='common':
            glasses = '戴了普通眼镜'
        else:
            glasses = '戴了墨镜'


        display_dicts.append({'age':int(face['age']), 'beauty':float(face['beauty']), 'expression':expression, 'gender':gender, 'glasses':glasses})

    
    #返回的字典数组
    return display_dicts

def _faces_to_audio_txt_dict(faces):
    """给一个face的json信息，输出音频的文本字典，字典每个值是一个数组，把多张脸的某类信息拼在一起。

    Args:
        face: json字典，形如：
            {
            'face_token': 'bc3b6b1b097c02a074ffe51600f05a5d',
            'location': {'left': 149.72, 'top': 203.17, 'width': 195, 'height': 173, 'rotation': -4},
            'face_probability': 1,
            'angle': {'yaw': -3.85, 'pitch': 23.26, 'roll': -5.66},
            'age': 26,
            'beauty': 86.31,
            'expression': {'type': 'none', 'probability': 1},
            'gender': {'type': 'male', 'probability': 1},
            'glasses': {'type': 'none', 'probability': 1}
            }
            
    输出字典形如：
        {
        'age':'年龄XX岁，年龄XX岁'...
        'beauty':'颜值XX分，颜值XX分'...
        'expression':'表情无（微笑，大小），表情无（微笑，大小）'...
        'glasses':'没有戴眼镜（戴了普通眼镜，戴了墨镜），没有戴眼镜（戴了普通眼镜，戴了墨镜）'...
        }
    """

    age = []
    beauty = []
    expression = []
    # gender = []
    # 'gender':'性别男（女）'
    glasses = []
    
    for face in faces:
        age.append(f"年龄{str(face['age'])}岁")
        
        beauty.append(f"颜值{str(face['beauty'])}分")
        
        if face['expression']['type'] == 'none':
            expression.append('表情无')
        elif face['expression']['type'] == 'smile':
            expression.append('表情微笑')
        else:
            expression.append('表情大笑')

        # if face['gender']['type'] == 'male':
        #     gender.append('性别男')
        # else:
        #     gender.append('性别女')

        if face['glasses']['type'] == 'none':
            glasses.append('没有戴眼镜')
        elif face['glasses']['type'] == 'common':
            glasses.append('戴了普通眼镜')
        else:
            glasses.append('戴了墨镜')
            
    audio_dict ={
        'age': '，'.join(age),
        'beauty': '，'.join(beauty),
        'expression': '，'.join(expression),
        # 'gender': '{}，'.join(gender),
        'glasses': '，'.join(glasses)
    }
    return audio_dict

def _save_file(bytes: bytes, suffix):
    """给定文件二进制流和后缀名（不带点），保存文件在static/files，返回文件名('xxx.mp3')
    """
    folderName = os.path.join(os.getcwd(), 'static/files/')
    
    fileName = '{}.{}'.format(uuid.uuid4(), suffix)
    fileFullName = os.path.join(folderName, fileName)

    if not os.path.exists(folderName):
        os.mkdir(folderName)

    try:
        with open(fileFullName, 'wb') as f:
            f.write(bytes)
        return fileName
    except Exception as e:
        raise e

def faces_to_audio_file_dict(token, faces):
    """多个 人脸json数据 转换成 一个字典。每个值存 细分后的音频 的文件名。

    先把多张人脸json数据转换成需要的音频文本字典，
    再把字典中的文本信息转换成音频二进制流，
    再把音频存到本地，
    再用一个字典存储多张脸的所有音频文件的名字
    最后返回存储 音频名字 字典构成的数组。
    
    输出字典形如：
        {
        'age':'年龄XX岁，年龄XX岁'...  的mp3文件名
        'beauty':'颜值XX分，颜值XX分'...  的mp3文件名
        'expression':'表情无（微笑，大小），表情无（微笑，大小）'...  的mp3文件名
        'glasses':'没有戴眼镜（戴了普通眼镜，戴了墨镜），没有戴眼镜（戴了普通眼镜，戴了墨镜）'...  的mp3文件名
        }
    """

    audio_txt_dict = _faces_to_audio_txt_dict(faces)
    audio_file_dict = {}
    
    for key, txt in audio_txt_dict.items():
        audio_bin_flow = tts.convert(token, txt, AUE=3)
        fileName = _save_file(audio_bin_flow, 'mp3')
        audio_file_dict[key] = fileName
            
    return audio_file_dict


