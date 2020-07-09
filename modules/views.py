from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core import serializers

import json

from modules import utils
from modules import faceDetect
from modules import tts
from modules import dongmanhua


# TODO 用户登录，存储历史记录

def index(request):
    return render(request, 'index.html')


def error(request, msg):
    return render(request, 'error.html', {'error_msg': msg})


def getToken(request):
    """获取两个token，存入cookie，返回HttpResponse结果
    """
    faceToken = request.COOKIES.get('face', None)
    ttsToken = request.COOKIES.get('tts', None)
    dongmanToken = request.COOKIES.get('dongman', None)

    resp = HttpResponse(json.dumps({"error": False}))

    if not faceToken:
        try:
            faceTokenDict = faceDetect.getToken()
            resp.set_cookie('face', faceTokenDict['token'], max_age=faceTokenDict['max_age'])

        except Exception as e:
            return HttpResponse(json.dumps({'error': True, 'url': '/error/{}/'.format(e)}))

    if not ttsToken:
        try:
            ttsTokenDict = tts.getToken()
            resp.set_cookie('tts', ttsTokenDict['token'], max_age=ttsTokenDict['max_age'])

        except Exception as e:
            return HttpResponse(json.dumps({'error': True, 'url': '/error/{}/'.format(e)}))

    if not dongmanToken:
        try:
            dongmanTokenDict = dongmanhua.getToken()
            resp.set_cookie('dongman', dongmanTokenDict['token'], max_age=dongmanTokenDict['max_age'])

        except Exception as e:
            return HttpResponse(json.dumps({'error': True, 'url': '/error/{}/'.format(e)}))

    return resp


def camera_site(request):
    """进入摄像头拍照页面
    """
    return render(request, 'camera.html')


def detect_camera(request):
    """根据post来的摄像头的照片dataURL，后台检测人脸，把人脸json数组和音频url路径数组存入session，后跳转到/result/
    """
    if request.POST:
        # # DEBUG:
        # face_list = [{
        #     'debug': '这是假数据',
        #     'face_token': 'bc3b6b1b097c02a074ffe51600f05a5d',
        #     'location': {'left': 149.72, 'top': 203.17, 'width': 195, 'height': 173, 'rotation': -4},
        #     'face_probability': 1,
        #     'angle': {'yaw': -3.85, 'pitch': 23.26, 'roll': -5.66},
        #     'age': 26,
        #     'beauty': 86.31,
        #     'expression': {'type': 'none', 'probability': 1},
        #     'gender': {'type': 'male', 'probability': 1},
        #     'glasses': {'type': 'none', 'probability': 1}
        # }]
        # audio_files = [
        #     utils._save_file(
        #         tts.convert("24.ecd50730e52b304cf1d3da9bbe399b8d.2592000.1596556460.282335-10854623",
        #                 "阿巴阿巴"),
        #         'mp3'
        #     )
        # ]

        # # 把结果存入session，然后跳转到/result/
        # request.session['face_list'] = face_list
        # request.session['audio_files'] = audio_files
        # request.session['result_expired'] = False  # 是否显示过这个结果，如果显示过应该认为session里的值是过期的
        # return redirect('/result/')
        debug_crop_only = False

        dataURL = request.POST.get('picDataURL', None)
        # print(dataURL)
        if dataURL:
            # 有图片，调用图像识别api
            faceToken = request.COOKIES.get('face', None)
            ttsToken = request.COOKIES.get('tts', None)
            dongmanToken = request.COOKIES.get('dongman', None)

            if not faceToken or not ttsToken or not dongmanToken:
                return redirect('/error/没有获取Token，需要进入首页获取')

            try:
                # 每个元素是一张脸对应的json数据
                faces = utils.dataURL_to_faces(faceToken, dataURL)

            except Exception as e:
                return redirect('/error/dataURL_to_faces出错: {}/'.format(e))
            
            if not debug_crop_only:
                try:
                    # 前端要播放的音频（每个元素是一个字典，字典每个元素是音频文件名）
                    audio_files = utils.faces_to_audio_file_dict(ttsToken, faces)
                except Exception as e:
                    return redirect('/error/faces_to_audio_files出错: {}/'.format(e))
            
            try:
                # 前端要显示的文本（字典存不同类型数据，每个值是一个数组，数组每个元素对应一张脸）
                face_display_dict = utils.faces_to_display_dict(faces)
            except Exception as e:
                return redirect('/error/faces_to_display_dict出错: {}/'.format(e))
            
            try:
                # 前端要显示的评语
                praise_dicts = utils.faces_to_praise_dicts(faces)
            except Exception as e:
                return redirect('/error/faces_to_display_dicts出错: {}/'.format(e))

            anim_file = []
            result_imgfiles = []
            
            if not debug_crop_only:
                try:
                    # 动漫化的图片文件名
                    anim_file = utils.dataURL_to_anim_file(dongmanToken, dataURL)
                except Exception as e:
                    return redirect('/error/dataURL_to_anim_file出错: {}/'.format(e))

    
                try:
                    # 人脸融合的图片文件名
                    result_imgfile1 = utils.dataURL_to_merge_face_file(faceToken, '胡歌.jpg', dataURL)
                    result_imgfile2 = utils.dataURL_to_merge_face_file(faceToken, '赫本.jpg', dataURL)
                    result_imgfile3 = utils.dataURL_to_merge_face_file(faceToken, '彭于晏.jpg', dataURL)
                    
                    result_imgfiles = [result_imgfile1, result_imgfile2, result_imgfile3]
                except Exception as e:
                    return redirect('/error/dataURL_to_merge_face出错：{}/'.format(e))

            # 保存图片，获取裁剪后的图片列表
            crop_imgs = utils.get_crop_filenames(dataURL, faces)

            try:
                # 把结果存入session，然后跳转到/result/
                # request.session['face_list'] = faces
                request.session['audio_files'] = audio_files
                request.session['face_display_dict'] = face_display_dict
                request.session['praise_dicts'] = praise_dicts
                request.session['anim_file'] = anim_file
                request.session['result_imgfiles'] = result_imgfiles
                request.session['crop_imgs'] = crop_imgs

                # 是否显示过这个结果，如果显示过应该认为session里的值是过期的
                request.session['result_expired'] = False
                return redirect('/result/')
            
            except Exception as e:
                return redirect('/error/存入session出错: {}/'.format(e))
            
        else:
            # 没有传来picDataURL数据，跳转回前端摄像头拍照页面
            return redirect('/camera/')
    else:
        # GET 方法，不处理数据，返回前端摄像头拍照页面
        return redirect('/camera/')

# 上传的照片也改为dataurl上传了
# def detect_picfile(request):
#     """根据post来的上传的照片二进制流，后台检测人脸，把人脸json数组和音频url路径数组存入session，后跳转到/result/
#     """
#     if request.POST:
#         # 获取来自input标签的文件内容
#         picfile = request.FILES.get('picfile', None)
#         # print(picfile)
#         if picfile:
#             # 有图片，调用图像识别api
#             faceToken = request.COOKIES.get('face', None)
#             ttsToken = request.COOKIES.get('tts', None)
#             try:
#                 # 每个元素是一张脸对应的json数据
#                 faces = utils.picfile_to_faces(faceToken, picfile)

#                 # 前端要播放的音频字典（字典每个值是音频文件名）
#                 audio_file_dict = utils.faces_to_audio_file_dict(ttsToken, faces)
#                 print("人脸数据" + faces)

#                 # 前端要显示的文本（字典存不同类型数据，每个值是一个数组，数组每个元素对应一张脸）
#                 face_display_dict = utils.faces_to_display_dict(faces)
                
                
#                 # 把结果存入session，然后跳转到/result/
#                 # request.session['face_list'] = faces
#                 request.session['face_display_dict'] = face_display_dict
#                 request.session['audio_files'] = audio_file_dict
#                 # 是否显示过这个结果，如果显示过应该认为session里的值是过期的
#                 request.session['result_expired'] = False
#                 return redirect('/result/')

#             except Exception as e:
#                 return redirect('/error/出错: {}/'.format(e))
#         else:
#             # 没有传来picDataURL数据，跳转回前端摄像头拍照页面
#             return redirect('/camera/')
#     else:
#         # GET 方法，不处理数据，返回前端摄像头拍照页面
#         return redirect('/camera/')

def result(request):
    """ 根据session显示相应的结果页面

    如果session['result_expired']为空或True则跳转回 /camera/
    """

    # 不考虑结果是否显示，刷新之后还停留在结果页面
    result_dont_expire = True
    
    # 判断session是否有数据
    if result_dont_expire or not request.session.get('result_expired', None):
        
        # print(request.session.get('face_display_dict', None))
        # print(request.session.get('audio_files', None))
        # print(request.session.get('praise_dicts', None))

        face_display_dict = request.session.get('face_display_dict', None)
        praise_dicts = request.session.get('praise_dicts', None)
        crop_imgs = request.session.get('crop_imgs', None)
        
        print(crop_imgs)
        
        res = {}
        
        for key, val in face_display_dict.items():
            res[key] = zip(val, praise_dicts[key], crop_imgs)
            # print(list(res[key]))
                
        # print(res)
        
        context = {}
        context['face_display_dict'] = res
        
        context['audio_files'] = request.session.get('audio_files', None)
        # context['praise_dicts'] = 
        context['anim_file'] = request.session.get('anim_file', None)
        context['result_imgfiles'] = request.session.get('result_imgfiles', None)

        request.session['result_expired'] = True
        
        return render(request, 'result.html', context)
    else:
        return redirect('/camera/')
    pass
