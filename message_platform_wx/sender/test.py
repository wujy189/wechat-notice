# Create your views here.
# coding:utf-8

import urllib, requests, json, sys
from datetime import datetime

now = datetime.now()
date_time = now.strftime('%Y-%m-%d %H:%M:%S')


# 获取所有执行参数
def get_argv():
    num, str1 = 1, ('Time:' + date_time)
    while (num < len(sys.argv)):
        str1 = str1 + ' \n' + sys.argv[num]
        num += 1
    return str1


class WeChat(object):
    __token_id = ''

    # init attribute
    def __init__(self, url):
        self.__url = url.rstrip('/')
        self.__corpid = 'ww51c3d280edda69c4'
        self.__secret = 'w0b8ZCQEJnZvLmRR2UBAuIb9Z4sIV93TBvDD2MMWo9U'

    # Get TokenID
    def authID(self):
        params = {'corpid': self.__corpid, 'corpsecret': self.__secret}
        # data = urllib.urlencode(params)
        content = self.getToken(params)
        try:
            self.__token_id = content['access_token']
            print(content['access_token'])
        except KeyError:
            raise KeyError

    # Establish a connection
    def getToken(self, data, url_prefix='/'):
        url = self.__url + url_prefix + 'gettoken?'
        try:
            response = requests.get(url, params=data)
        except KeyError:
            raise KeyError
        content = json.loads(response.text.encode('utf8'))
        return content

    # Get sendmessage url
    def postData(self, data, url_prefix='/'):
        url = self.__url + url_prefix + 'message/send?access_token=%s' % (self.__token_id)
        try:
            result = requests.get(url, params=data)
            print(result.status_code)
        except Exception as e:
            print(e)

    # send message
    def sendMessage(self, message):
        self.authID()
        data = {
            'touser': '@all',
            'toparty': "1",
            'msgtype': "text",
            'agentid': "1000003",
            'text': {
                'content': message
            },
            'safe': "0"
        }
        self.postData(data)


if __name__ == '__main__':
    a = WeChat('https://qyapi.weixin.qq.com/cgi-bin')
    message = get_argv()
    a.sendMessage(message)

# def send(request):
#         a = WeChat('https://qyapi.weixin.qq.com/cgi-bin')
#         content = request.GET.get("content","").encode("utf-8")
#         message = ('Time:'+date_time) + "\n" + content
#         a.sendMessage(message)
