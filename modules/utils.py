import os
import uuid
import json
import random

from modules import faceDetect
from modules import tts
from modules import dongmanhua


def dataURL_to_anim_file(token, dataURL):
    image64 = faceDetect.dataURL_to_image64(dataURL)
    file = dongmanhua.selfie_anime(token, image64)
    fileName = _save_file(file, "animfile.jpg")
    return fileName

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
#
# def picfile_to_faces(token, picfile):
#     """根据图片文件流获取识别数据，数组的每个元素对应一张脸。
#     """
#     image64 = faceDetect.picfile_to_image64(picfile)
#
#     result = faceDetect.detect(token, image64)
#
#
#
#     face_list = result['face_list']
#
#     return face_list

def faces_to_display_dict(faces):
    """给一个数组，每个元素是一张脸的json信息，输出的是字典，字典每个值是一个数组，把多张脸的某类文本信息拼在一起。

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
            'age_gender':[(int, 男（女）), ...]
            'beauty':[float, ...]
            'expression':['无（微笑，大小）', ...]
            'glasses':['没有戴眼镜（戴了普通眼镜，戴了墨镜）', ...]
            }
        """
    
    display_dict = []
    
    age_gender = []
    beauty = []
    expression = []
    glasses = []
    
    
    for face in faces:
        if face['gender']['type']=='male':
            age_gender.append((face['age'], '男'))
        else:
            age_gender.append((face['age'], '女'))

        beauty.append(face['beauty'])
        
        if face['expression']['type']=='none':
            expression.append('无')
        elif face['expression']['type']=='smile':
            expression.append('微笑')
        else:
            expression.append('大笑')

        if face['glasses']['type']=='none':
            glasses.append('没有戴眼镜')
        elif face['glasses']['type']=='common':
            glasses.append('戴了普通眼镜')
        else:
            glasses.append('戴了墨镜')


    display_dict = {
        'age_gender': age_gender,
        'beauty': beauty,
        'expression': expression,
        'glasses': glasses
    }
    
    #返回的字典数组
    return display_dict


def faces_to_praise_dicts(faces):
    """给一个face的json信息，输出彩虹屁的文本字典，字典每个值是一个数组，把多张脸的某类信息拼在一起。

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
        'age':'彩虹屁，彩虹屁'...
        'beauty':'彩虹屁，彩虹屁'...
        'expression':彩虹屁，彩虹屁'...
        'glasses':彩虹屁，彩虹屁'...
        }
    """

    ages = ['保持同心，年龄就只是数字。',
            '相信你每一岁的生活都丰富多彩。',
            '结果与实际不符？建议重新摆个pose再来一次。',
            '我转山转水转佛塔，不为修来生，只为在对的时间遇见对的你。',
            '时光会在脸上留下痕迹，但不会在信件留痕，每个人都在思维上永葆青春。']

    # 低于40分
    beauty1 = ['检测结果有误，我相信您是最美的。',
               '测试结果仅为百度AI返回数据，不代表本项目审美观点，如对结果不满，请找百度。',
               '本程序不能检测你的美丽心灵。']
    # 40-60分
    beauty2 = ['世间没有哪两朵花是一样的也许你与别人获得相同的分数，但你拥有的是独属于你的美丽。',
               '我问佛，为何不给所有人倾城的容颜？佛曰：那只是昙花的一现，用来蒙蔽世俗的眼，没什么美可以低过一颗纯净仁爱的心，我把它赐给了你。']
    # 60-80分
    beauty3 = ['You are so beautiful!',
               '不管分高或者分低，你都在我眼里，来我怀里，或者，让我住进你的心里。',
               '​今天吃了果冻打了电动对你心动。',
               '​今天也为你的颜值原地360度跳起了爱的魔力转圈圈']
    # 80-100分
    beauty4 = ['您从小就是校草/校花吧！',
               '您的颜值已爆表！',
               '哇噻！您莫不是天神下凡。',
               '​恐龙会灭绝绝对是因为前肢太短没法为你的美丽鼓掌。']

    # 没有表情
    expression1 = ['微笑了再测试一次颜值会提高哟！',
                   '是有什么烦心事吗？可以说给我听啊，我一直都在。',
                   '一本正经的高冷面孔~',
                   '面无表情却又英气逼人。',
                   '来，茄～子～']
    # 微笑
    expression2 = ['你笑起来真好看，像春天的花一样~'
                   '爱笑的人，运气不会太差哦。',
                   '笑口常开，好彩自然来。',
                   '只有在你的微笑里，我才有呼吸。',
                   '美人微笑转星眸。',
                   '你笑起来的样子最为动人。']
    # 大笑
    expression3 = ['什么事那么开心呀？可以与我分享一下吗？',
                   '你开心了我就开心了。',
                   '明眸皓齿，说的就是你吧。',
                   '哈哈哈哈哈，想必今天心情很好吧～',
                   '冬天的糖霜，秋天的麦芽糖，夏天的莲子羹，春天的绿豆酥，都甜不过你的笑。']

    # 没有戴眼镜
    glasses1 = ['要继续保护好眼睛，每天做个眼保健操。',
                '很荣幸见证了你原始的美丽。',
                '你的眼睛很美,像海一样，请你相信,岛屿密集的海都没有那么蓝。',
                '说星星好看的人一定没见过你的眼睛。']
    # 戴了普通眼镜
    glasses2 = ['眼镜也不能遮挡你美丽明亮的双眼。',
                '上帝舍不得让你的双眼接触到世间的尘埃，所以送给了你一副眼镜。',
                '你的学识已经透过镜片和屏幕传达到了我的面前。',
                '要记得多放松眼睛哦。']
    # 戴了墨镜
    glasses3 = ['哇哦，你怎么这么飒。',
                '墨镜一戴，谁都不爱。',
                '刺眼的阳光不再锐利，代之以柔和的光晕。',
                '酷盖拍照都不摘墨镜。']
    age = []
    beauty = []
    expression = []
    glasses = []
    for face in faces:
        age.append(random.choice(ages))

        beauty_grade = float(face['beauty'])
        if beauty_grade < 40:
            beauty.append(random.choice(beauty1))
        elif beauty_grade >= 40 and beauty_grade < 60:
            beauty.append(random.choice(beauty2))
        elif beauty_grade >= 60 and beauty_grade < 80:
            beauty.append(random.choice(beauty3))
        else:
            beauty.append(random.choice(beauty4))

        if face['expression']['type'] == 'none':
            expression.append(random.choice(expression1))
        elif face['expression']['type'] == 'smile':
            expression.append(random.choice(expression2))
        else:
            expression.append(random.choice(expression3))

        if face['glasses']['type'] == 'none':
            glasses.append(random.choice(glasses1))
        elif face['glasses']['type'] == 'common':
            glasses.append(random.choice(glasses2))
        else:
            glasses.append(random.choice(glasses3))
    praise_dicts = {
        'age': age,
        'beauty': beauty,
        'expression': expression,
        'glasses': glasses
    }

    # 返回的字典数组
    return praise_dicts


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
        'glasses': '，'.join(glasses)
    }
    return audio_dict

def _save_file(bytes: bytes, filename):
    """给定文件二进制流和后缀名（不带点），保存文件在static/files，返回文件名('xxx.mp3')
    """
    folderName = os.path.join(os.getcwd(), '/2020sp02-n/static/files/')
    
    fileFullName = os.path.join(folderName, filename)

    if not os.path.exists(folderName):
        os.mkdir(folderName)

    try:
        with open(fileFullName, 'wb') as f:
            f.write(bytes)
        return filename
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
        fileName = _save_file(audio_bin_flow, f'{key}.mp3')
        audio_file_dict[key] = fileName
    
    return audio_file_dict

# 人脸融合
def dataURL_to_merge_face_file(token, image_template_name, dataURL):
    """根据摄像头照片dataURL获取目标图，处理得到融合图像的base64编码，返回保存的文件名
    """
    image_target64 = faceDetect.dataURL_to_image64(dataURL)
    
    folderName = os.path.join(os.getcwd(), 'static/images/')
    fileFullName = os.path.join(folderName, image_template_name)
    image_template64 = faceDetect.imgfile_to_image64(fileFullName)

    image_merge = faceDetect.merge(token, image_template64, image_target64)

    image_merge_filename = _save_file(image_merge, 'merge_' + image_template_name)

    return image_merge_filename


# def picfile_to_merge_face(token, image_template, picfile):
#     """根据图片文件流获取目标图，返回模板图和目标图的融合图像base64编码
#     """
#     image_target64 = faceDetect.picfile_to_image64(picfile)
#     image_template64 = faceDetect.picfile_to_image64(image_template)

#     image_merge = faceDetect.merge(token, image_template64, image_target64)

#     return image_merge
