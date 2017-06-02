# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 18:17:45 2017

@author: 51433
"""

#coding:utf-8
import random
import time
import urllib.request
import re
import logging
n=0
base_url = 'http://xk.shu.edu.cn:8080'
url=base_url + '/CourseSelectionStudent/CtrlViewOperationResult'
SessionId = ''
CourseStr = '08306030'
TeacherStr = '1002'
StudentNo = '15123005'
logging.basicConfig(filename = 'xk.log', level = logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def bang():
    headers = {'Origin': 'http://xk.shu.edu.cn:8080', 'Content-Length': '110', 'Accept-Language': 'zh-CN,zh;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'X-Requested-With': 'XMLHttpRequest', 'Host': 'xk.shu.edu.cn', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2552.0 Safari/537.36', 'Connection': 'keep-alive', 'Cookie': 'Hm_lvt_444bf10f6d7469654b7f41f9f9f9c301=1449989162,1449989164,1451806133,1452091199; ASP.NET_SessionId=' +SessionId , 'Referer': 'http://xk.shu.edu.cn:8080/CourseSelectionStudent/FuzzyQuery', 'Content-Type': 'application/x-www-form-urlencoded'}
    #data= {'stuNo': '15123005', 'IgnorCourseGroup': 'false', 'ListCourseStr': CourseStr, 'IgnorClassMark': 'false', 'IgnorCredit': 'false'}
    data2='ListCourseStr=' + CourseStr +'%7C' + TeacherStr + '%7C0&stuNo='+StudentNo + '&IgnorClassMark=false&IgnorCourseGroup=false&IgnorCredit=false'
    data2 = data2.encode()
    request=urllib.request.Request(url,data2,headers)
    response = urllib.request.urlopen(request)
    res=response.read()
    #res=zlib.decompress(res,zlib.MAX_WBITS|32)
    res = res.decode()
    print(res)
    comingsoon = re.search('选课时间未到', res)
    susmat = re.search('成功',res)
    errmat = re.search('请输入',res)
    errmat2 = re.search('异常',res)
    contmat= re.search ('已满',res)
    havemat=re.search('已选',res)
    if comingsoon:
        logging.debug('选课时间未到')
        return False
    if susmat!= None :
        logging.debug ('成功选课')
        return True
    if errmat != None or errmat2 != None:
        logging.debug ('异常出现拉，赶紧来看看！！')
        return True
    if contmat !=None :
        logging.debug( '正常选课中.....')
        return False
    if havemat != None:
        logging.debug ('已经选好拉')
        return True

while True :
    ret = bang()
    n += 1
    t=random.uniform(5,6)
    if ret :
        #winsound.PlaySound('1.wav',winsound.SND_LOOP)
        break
    time.sleep(t/2)
    print(n)
    time.sleep(t/2)
