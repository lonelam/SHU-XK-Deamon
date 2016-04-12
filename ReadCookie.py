# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import time
import webbrowser
import zlib
from Auto_CHPTCHA import *
username = '12345'
psw = '12345'
class Shu:
    def __init__(self,usn,pssw):
        self.TxtUsername=usn
        self.TxtPassword=pssw
        self.Date =time.strftime('%a, %d %b %Y %X GMT')
        self.SessionId=''
        self.IndexUrl='http://xk.shu.edu.cn:8080/Login/Index'
        self.CodeUrl='http://xk.shu.edu.cn:8080/Login/GetValidateCode?%20%20+%20GetTimestamp()'
        self.LoginHeaders={
            'Cache-Control':'private',
            'Content-Encoding':'gzip',
            'Content-Type':'text/html; charset=utf-8',
            'Date': self.Date,
            'Server':'Microsoft-IIS/7.5',
            'Transfer-Encoding':'chunked',
            'Vary':'Accept-encoding',
            'X-AspNet-Version':'4.0.30319',
            'X-AspNetMvc-Version':'3.0',
            'X-Powered-By':'ASP.NET'
        }
      
        self.IndexBody={
            'txtUserName':self.TxtUsername,
            'txtPassword':self.TxtPassword
        }
        self.get ={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie': '_ga=GA1.3.548295607.1450860734; Hm_lvt_444bf10f6d7469654b7f41f9f9f9c301=1449989162,1449989164,1451806133,1452091199; ASP.NET_SessionId='+self.SessionId,
            'Host':'xk.shu.edu.cn:8080',
            'Referer':'http://xk.shu.edu.cn:8080/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2552.0 Safari/537.36'
        }
        self.Getheader = urllib.urlencode(self.get)
        self.fn='cookie.txt'
        self.cookie =cookielib.LWPCookieJar(self.fn)
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookieHandler,urllib2.HTTPHandler)

    def login(self):
        Indexbody = urllib.urlencode(self.IndexBody)
        request = urllib2.Request(self.IndexUrl,Indexbody)
        response=self.opener.open(request)
        content=response.read()
        return content
    def getIdenCode(self):
        pic=urllib2.Request(self.CodeUrl,self.Getheader)
        return pic
    def main(self):
        self.opener.open('http://xk.shu.edu.cn:8080/')
        self.cookie.save(ignore_discard=True, ignore_expires=True)
        cookie=open('cookie.txt').read()
        print cookie
        pattern= re.compile('ASP.NET_SessionId=(........................);*?')
        self.SessionId = re.search(pattern,cookie).group(1)
        self.get ={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie': '_ga=GA1.3.548295607.1450860734; Hm_lvt_444bf10f6d7469654b7f41f9f9f9c301=1449989162,1449989164,1451806133,1452091199; ASP.NET_SessionId='+self.SessionId,
            'Host':'xk.shu.edu.cn:8080',
            'Referer':'http://xk.shu.edu.cn:8080/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2552.0 Safari/537.36'
        }
        self.Getheader = urllib.urlencode(self.get)
        img = self.opener.open('http://xk.shu.edu.cn:8080/Login/GetValidateCode?%20%20+%20GetTimestamp()')
        local = open('Code.jpg', 'wb')
        local.write(img.read())
        local.close()
        code = Auto_CHPTCHA('Code.jpg')
        self.IndexBody['txtValiCode']=str(code)
        content = self.login()
        return content
#username = raw_input('学号：')
#psw =raw_input('密码：')
username = '15124550'
psw = 'Nbanba5636'
shu=Shu(username,psw)
content = shu.main()
while content.find('Validate') != -1:
    print content.find('Validate')
    print shu.IndexBody['txtValiCode']
    content = shu.main()
print content
