#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/18 9:54
__Author__=
__Des__=
"""
import requests
import json
from comn.log import Log
import allure
from comn.init_path import BASHPATH
from comn.conf import Configure
# from comn.get_token import get_token

class RequestClass(object):
    def __init__(self):
        self.log = Log()
        self.conf=Configure()

    def __req_get(self, url, data=None, headers=None):
        '''
        请求方式为get的请求
        :param url: 请求url
        :param params: 请求参数
        :param headers: 请求头
        :return:
        '''
        if data:
            req=requests.get(url,params=data,headers=headers)
        else:
            req=requests.get(url,headers=headers)
        return req

    def __req_post(self, url, data=None, headers=None, file=None, Content_Type=None):
        if file:
            try:
                files={
                    "file": (file, open(BASHPATH+file, "rb"), "application/octet-stream")
                    # 以二进制形式打开文件：图片
                    # "pic": ("test01.gif", open("test01.gif", "rb"), "images/git")
                }
            except Exception as e:
                self.log.logger.error(e)

            req = requests.post(url,data=data,headers=headers,files=files)
        else:
            if data:
                if Content_Type=="application/x-www-form-urlencoded":
                    req = requests.post(url, data=data, headers=headers)
                else:
                    req = requests.post(url, json=data, headers=headers)
            else:
                req = requests.post(url, headers=headers)
        return req


    def __req_put(self, url, data=None, headers=None):
        if data:
            data=json.dumps(data)
            req=requests.put(url, data=data, headers=headers)
        else:
            req=requests.put(url,headers=headers)

        return req



    def __req_delete(self, url, data=None, headers=None):
        if data:
            data=json.dumps(data)
            req= requests.delete(url, data=data, headers=headers)
        else:
            req=requests.delete(url,headers=headers)
        return req



    def Sendrequest(self,method,url,headers=None,data=None,files=None,Content_Type=None,isallure=True,**kwargs):
        '''
        request请求方法封装
        :param method: 请求方法
        :param url: 请求url
        :param data: 请求参数
        :param headers: 请求头
        :param files: 要上传的文件
        :param Content_Type: 请求头请求方式
        :param isallure: 是否写入allure报告
        :param kwargs:可变的关键字参数，字典
        :return:
        '''
        print("======",data)
        try:
            url=self.conf.HOST+url
            if method.lower()=="get":
                req=self.__req_get(url, data, headers)
            elif method.lower()=="post":
                req=self.__req_post(url, data=data, headers=headers, file=files, Content_Type=Content_Type)
            elif method.lower()=="put":
                req=self.__req_put(url, data, headers)
            elif method.lower().lower()=="delete":
                req=self.__req_delete(url, data, headers)
            if isallure:
                # 子功能
                allure.dynamic.story(dict(**kwargs).get("story"))
                # 接口标题
                allure.dynamic.title(dict(**kwargs).get("title"))
                # 接口描述
                allure.dynamic.description(dict(**kwargs).get("description"))
                allure.attach(name="请求url", body=f"{url}")
                allure.attach(name="请求头", body=f"{headers}")
                allure.attach(name="请求参数", body=f"{data}")
                exportfile=dict(**kwargs).get("exportfile")
                if exportfile:
                    with open(exportfile, 'wb') as fn:
                        fn.write(req.content)
                        # allure.attach.file('d:\\1.png', " png 图片", allure.attachment_type.PNG)  #添加附件
                        allure.attach.file(exportfile, " csv 文件", allure.attachment_type.CSV)  # 添加附件,附件类型为csv


            if req.status_code != 200:
                self.log.logger.warning("\n[请求url]:{} \n[请求参数]:{} \n[相应码]:{} \n[相应内容]{}".format(url,json.dumps(data,indent=4,ensure_ascii=False), req.status_code, req.text))
                return req.status_code, req.text
            else:
                # self.log.logger.info("\n[请求url]:{} \n[请求参数]:{} \n[相应码]:{} \n[相应内容]{}".format(url, json.dumps(data,indent=4,ensure_ascii=False), req.status_code,json.dumps(req.json(),indent=4,ensure_ascii=False)))
                return req.status_code, req.json()
        except Exception as e:
            self.log.logger.error("\n[请求url]:{} \n[请求参数]:{} \n[异常错误]{}".format(url, json.dumps(data,indent=4,ensure_ascii=False),e))