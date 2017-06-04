# -*- coding:utf-8 -*-
import urllib
import re
import time
import os
import os.path
import zlib
import configparser
import http.cookiejar
from PIL import Image
import pytesseract
import logging
import platform
#from Auto_CHPTCHA import *
if platform.system() == 'Windows':
    import matplotlib.pyplot as plt
threshold=110
cfg = configparser.ConfigParser()
cfg.read('config.ini')
password = str(cfg.get('user', 'password'))
username = str(cfg.get('user', 'username'))
class_ids = eval(cfg.get('courses', 'course_list'))#['08306030',]
teacher_ids = eval(cfg.get('courses', 'teacher_ids'))#['1002',]
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
model_dict = {}
def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    tmpset = set()
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            #print(pixdata[x, y - 1])
            if pixdata[x,y-1] == 0:
                count = count + 1
            if pixdata[x,y+1] == 0:
                count = count + 1
            if pixdata[x-1,y] == 0:
                count = count + 1
            if pixdata[x+1,y] == 0:
                count = count + 1
            if count > 2:
                tmpset.add((x,y))
    for i in tmpset:
        pixdata[i] = 0
    return img
logging.basicConfig(filename = 'xk.log', level = logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

base_url = 'http://xk.autoisp.shu.edu.cn:8080'

class sim_client:
    def __init__(self, username, password):
        #self.model_dict = model_dict
        self.TxtUsername = username
        self.TxtPassword = password
        self.IndexUrl = base_url
        self.CodeUrl = base_url + '/Login/GetValidateCode?%20%20+%20GetTimestamp()'
        self.IndexBody = {'txtUserName':self.TxtUsername,'txtPassword':self.TxtPassword}
        self.cookie = http.cookiejar.LWPCookieJar()
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.cookieHandler, urllib.request.HTTPHandler)
    def run(self):
        
        while True:
            self.opener.open(self.IndexUrl)
            temp_file = open('temp_code.jpg', 'wb')
            temp_file.write(self.opener.open(self.CodeUrl).read())
            temp_file.close()
            img = Image.open('temp_code.jpg')
            img = img.convert('L')
            #img = img.filter(ImageFilter.MedianFilter())
            img = img.point(table, '1')
            #img = depoint(img)
            #img.show()
            if platform.system() == 'Windows':
                plt.imshow(img)
                plt.show()
                plt.close()
            validate_code = pytesseract.image_to_string(img, config='-psm 7')
            if (len(validate_code)!=4):
                continue
            logging.debug(validate_code)
          #  validate_code = input('manually type in the validate code you see\n')
            self.IndexBody['txtValiCode'] = str(validate_code)
            break
        content = self.__login()
        return content
    def __login(self):
        Indexbody = urllib.parse.urlencode(self.IndexBody).encode()
        #print(Indexbody)
        request = urllib.request.Request(self.IndexUrl,Indexbody)
        response = self.opener.open(request)
        content = response.read()
        return content.decode()
def client_login(username, password):
    client = sim_client(username, password)
    content = client.run()
   # logging.debug(content)
    while content.find('上学期平均绩点') == -1:
        if (content.find('限制') != -1):
            logging.debug('被限制登陆了')
        content = client.run()
        logging.debug('登陆失败')
    logging.debug('login success')
    return client

#for course inquire, the parameter is class name. for course selection,it's the list of class
def request_constructor(username, request_type, parameter):
    query_url = base_url + '/StudentQuery/CtrlViewQueryCourse'
    select_url = base_url + '/CourseSelectionStudent/CtrlViewOperationResult'
    if request_type == 'query_course':
        raw_data_sheet = 'CourseName=%' + urllib.request.quote(parameter) + '&'
        access_url = query_url
    if request_type == 'select_course':
        raw_data_sheet = 'IgnorClassMark=False&IgnorCourseGroup=False&IgnorCredit=False&StudentNo=' + username + '&'
        for i in range(len(parameter)):
            raw_data_sheet = raw_data_sheet + 'ListCourse%5B' + str(i) + '%5D.CID=' + parameter[i][0] + '&ListCourse%5B' + str(i) + '%5D.TNo=' + parameter[i][1] + '&'
        access_url = select_url
    return urllib.request.Request(access_url,raw_data_sheet.encode())

def course_attack(username, password, class_list, idle_time = 7, reset_time = 10000):
    client = client_login(username, password)
    request = request_constructor(username, 'select_course', class_list)
    vain = client.opener.open(base_url + '/CourseSelectionStudent/FastInput')
    flag = True
    fliper = True
    while flag:
        try:
            reponse = client.opener.open(request).read().decode()
            #logging.debug(reponse)
            #if (len(re.findall('教学班人数已满', reponse)) != 0):
                #vain = client.opener.open(base_url + '/CourseSelectionStudent/FastInput')
            if fliper:
                logging.debug('持续尝试中...')
                fliper = False
            if len(re.findall('已选此课程', reponse)) == len(class_list):
                logging.debug ('check')
                fliper = True
                flag = False
            elif len(re.findall('已选此课程', reponse)) != 0:
                logging.debug('已选部分课程')
                fliper = True
            elif len(re.findall('限制', reponse)) != 0:
                logging.debug('被限制登陆了')
                fliper = True
                return None 
            #print(time.time() - embark)
            vain = client.opener.open(base_url + '/CourseSelectionStudent/FastInput')
            if len(re.findall('请输入',vain.read().decode())) != 0:
                logging.debug('登出了不知道为什么')
                fliper = True
                client = client_login(username, password)
                #vain = client.opener.open(base_url + '/CourseSelectionStudent/FastInput')
                #embark = time.time()
            time.sleep(idle_time)
        except TimeoutError:
            logging.debug('连接失败,TimeoutError')
            fliper = True
        except urllib.request.URLError:
            logging.debug('连接失败,URLErroor')
            fliper = True
    print ('结束')
    return None


#preload svm model

#get input
#pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
#username = '15123005'
#password = 'Ran0929'

class_list = [(class_ids[i], teacher_ids[i]) for i in range(len(class_ids))]

course_attack(username, password, class_list)
