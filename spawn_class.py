# -*- coding:utf-8 -*-
import urllib
import re
import time
import os
import os.path
import zlib
import http.cookiejar
from PIL import *
#from Auto_CHPTCHA import *
#from pass_input import *

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
        self.opener.open(self.IndexUrl)
        temp_file = open('temp_code.jpg', 'wb')
        temp_file.write(self.opener.open(self.CodeUrl).read())
        temp_file.close()
        
#        img = Image.open('temp_code.jpg')
#        img.show()
#        validate_code = Auto_CHPTCHA('temp_code.jpg',model_dict)
        validate_code = input('manually type in the validate code you see\n')
        self.IndexBody['txtValiCode'] = str(validate_code)
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
    while content.find('Validate') != -1:
        content = client.run()
    print ('login success')
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

def course_attack(username, password, class_list, idle_time = 7, reset_time = 7000):
    client = client_login(username, password)
    request = request_constructor(username, 'select_course', class_list)
    vain = client.opener.open(base_url + '/CourseSelectionStudent/FastInput')
    flag = True
    embark = time.time()
    while flag:
        reponse = client.opener.open(request).read().decode()
        print(reponse)
        if len(re.findall('已选此课程', reponse)) == len(class_list):
            print ('check')
            flag = True
        if len(re.findall('已选此课程', reponse)) != 0:
            vain = client.opener.open(base_url + '/CourseSelectionStudent/FastInput')
        if len(re.findall('限制', reponse)) != 0:
            print('hypocritical')
            return None 
        #print(time.time() - embark)
        if len(re.findall('请输入',reponse)) != 0:
            print('farewell')
            client = client_login(username, password)
            vain = client.opener.open(base_url + '/CourseSelectionStudent/FastInput')
            #embark = time.time()
        time.sleep(idle_time)
    print ('peace')
    return None

def wise_course_attack(username, password, class_list, idle_time = 5, reset_time = 7000):
    client = client_login(username, password)
    request = request_constructor(username, 'select_course', class_list)
    vain = client.opener.open(base_url + '/CourseSelectionStudent/FastInput')
    flag = True
    embark = time.time()
    while flag:
        #print client.opener.open(request).read()
        client.opener.open('http://xk.autoisp.shu.edu.cn:8080/Login/Logout') 
        vain = client.opener.open('http://xk.autoisp.shu.edu.cn:8080/Login/Index')
        client = client_login(username, password, model_dict)
        if client.opener.open('http://xk.autoisp.shu.edu.cn:8080/StudentQuery/QueryEnrollRank').read().find('排名') != -1:
            print (time.time())
        vain = client.opener.open('/CourseSelectionStudent/FastInput')
        #print vain.read()
    print ('peace')
    return None

#preload svm model
#model_dir = os.getcwd() + '\\model'
#print model_dir
#files = os.listdir(model_dir)
#model_dict = {}
#for file in files:
#    temp_model = svm_load_model(model_dir + '\\' + file)
#    model_dict[str(file).strip('.model')] = temp_model

#get input

username = '15123005'
password = 'Laizenan09'
class_ids = ['08306030',]
teacher_ids = ['1002',]
class_list = [(class_ids[i], teacher_ids[i]) for i in range(len(class_ids))]

course_attack(username, password, class_list)
