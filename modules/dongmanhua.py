import base64
import requests

def getToken():

    AK = 'TIrPv6OxYBVes9lLOsNGzh28'
    SK = 'GAVhVBiST8h5DqXsyFQrrSFzhrHo0gyC'
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(
        AK, SK)


    # host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TIrPv6OxYBVes9lLOsNGzh28&client_secret=GAVhVBiST8h5DqXsyFQrrSFzhrHo0gyC'
    respjson = requests.get(host).json()

    if ('access_token' in respjson.keys() and 'scope' in respjson.keys()):
        print(
            'SUCCESS WITH TOKEN: {} ; EXPIRES IN SECONDS: {}'.format(respjson['access_token'], respjson['expires_in']))

        return { 'token': respjson['access_token'], 'max_age': respjson['expires_in'] }
    else:
        raise Exception('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


# def picfile_to_image64(picfile):
#     """二进制流图片转image64
#     """
#     img64 = str(base64.b64encode(picfile.read()), 'utf-8')
#     return img64
#
    # if response:
    # access_token = response.json()["access_token"]


# 人像动漫化
def selfie_anime(token,image64):
    """输入image64，输出调用百度API后的人像动漫化图片二进制流

    """
    image_type = "BASE64"
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime"
    params = {"image":image64, 'image_type': image_type,}

    print("in 动漫化")

    request_url = request_url + "?access_token=" + token

    headers = {'content-type': 'application/x-www-form-urlencoded'}

    respjson = requests.post(request_url, data=params, headers=headers).json()
    # {
    #    'log_id',
    #    'image': /9j/4AAQSk...
    # }


    try:
        img64 = (respjson['image'])
        return base64.b64decode(img64)
    
    except Exception as e:
        raise e

if __name__ == '__main__':
    selfie_anime(getToken(),
        "data:image/gif;base64,R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAwAAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFzByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSpa/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJlZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uisF81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PHhhx4dbgYKAAA7")


