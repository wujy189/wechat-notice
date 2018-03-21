from django.shortcuts import render
# coding:utf-8
from django.http import HttpResponse

import requests,json,sys
import datetime

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
            result = requests.post(url, json=data)
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


# if __name__ == '__main__':
#     a = WeChat('https://qyapi.weixin.qq.com/cgi-bin')
#     message = get_argv()
#     a.sendMessage(message)

def send(request):
        dt = datetime.datetime.now() + datetime.timedelta(hours=8)
        date_time = dt.strftime('%Y-%m-%d %H:%M')
        if request.method == 'GET':
                a = WeChat('https://qyapi.weixin.qq.com/cgi-bin')
                content = request.GET.get("content","")
                message = ('Time:'+date_time) + "\n" + content
                a.sendMessage(message)
        elif request.method == 'POST':
                a = WeChat('https://qyapi.weixin.qq.com/cgi-bin')
                # content = request.POST.get("content", "")
                data = json.loads(request.body)
                content = data['content']
                message = ('Time:' + date_time) + "\n" + content
                a.sendMessage(message)
        return HttpResponse("信息发送成功！")