#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/20 9:44
__Author__=
__Des__=
"""
from selenium import webdriver
import time
import json
from comn.log import Log
from comn.oper_excel import Oper_Excel

class Scrapy_api(object):
    '''
    获取showdoc相关数据
    '''
    def __init__(self):
        self.log=Log()
        self.driver=webdriver.Chrome()
        #所有api数据
        self.apiall_list=[]
        self.exl=Oper_Excel()

    def getalllinks(self):
        '''
        获取所有接口文档连接地址,然后写入txt
        :return:
        '''
        self.driver.get("http://172.27.129.135/showdoc/index.php?s=/52")
        time.sleep(3)
        self.driver.implicitly_wait(15)
        menu_eles = self.driver.find_elements_by_tag_name("a")
        # list_url = []
        str_urls=""
        for ele in menu_eles:
            list = ["https://www.showdoc.cc/help", "http://172.27.129.135/showdoc/index.php?s=/home/user/login",
                    "http://172.27.129.135/showdoc/index.php?s=/52#", "https://www.showdoc.cc/page/63882"]
            if ele.get_attribute("href") not in list:
                str_urls+=ele.get_attribute("href")+"\n"
        # return str_urls
        with open("api.txt", 'w+', encoding='utf-8') as f:
            f.write(str_urls)

    def get_datas(self,url):
        '''
        获取某个接口连接页面的api接口内容
        :param url:
        :return:
        '''

        # self.driver.get("http://172.27.129.135/showdoc/index.php?s=/home/page/index/page_id/3382")
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
        except Exception as e:
            self.log.logger.error("页面{}不存在".format(url))
            return None
        #获取api接口的标题
        title=self.driver.find_element_by_id("page_title").text
        #获取api接口的描述 url 请求方法
        des_ele=self.driver.find_elements_by_css_selector("#page_md_content > ul> li")
        api_datas= [ele.text for ele in des_ele]



        request_datas={} #获取api接口的请求参数
        request_headers={} #获取api接口的请求头
        response_params = [] #获取api接口的响应数据格式

        try:
            ele_q = self.driver.find_element_by_xpath('//strong[contains(text(),"请求头")]/parent::p/following::div')
            eles = ele_q.find_elements_by_tag_name("tbody>tr")
            for ele in eles:
                param, des = ele.get_attribute("innerText").split("\t", 1)
                des = des.replace("\t", " ")
                request_headers[param] = des
        except Exception:
            self.log.logger.error("{} 未定位到元素，header为空request_headers".format(url))

        try:
            ele_q = self.driver.find_element_by_xpath('//strong[contains(text(),"参数：")]/parent::p/following::div')
            eles = ele_q.find_elements_by_tag_name("tbody>tr")
            for ele in eles:
                param, des = ele.get_attribute("innerText").split("\t", 1)
                des = des.replace("\t", " ")
                request_datas[param] = des
        except Exception:
            self.log.logger.error("{} 未定位到元素，参数为空request_datas".format(url))

        try:
            ele_q= self.driver.find_element_by_xpath('//strong[contains(text(),"返回参数说明")]/parent::p/following::div')
            eles=ele_q.find_elements_by_tag_name("tbody>tr")
            for ele in eles:
                param, des=ele.get_attribute("innerText").split("\t", 1)
                response_params.append(param)

        except Exception:
            self.log.logger.error("{} 未定位到元素，返回参数说明为空response_params".format(url))

        api_datas.insert(0, title)
        api_datas.append(json.dumps(request_headers,indent=4,ensure_ascii=False))
        api_datas.append(json.dumps(request_datas,indent=4,ensure_ascii=False))
        api_datas.append(json.dumps(response_params,indent=4,ensure_ascii=False))

        return api_datas



    def driver_quit(self):
        self.driver.quit()


if __name__ == '__main__':
    s_api=Scrapy_api()
    # with open('api.txt','r',encoding='utf-8') as f:
    #     str=f.read()
    # urls=str.split('\n')
    #
    # for num,url in enumerate(urls):
    #     if 147<=num<150:
    #         s_api.apiall_list.append(s_api.get_datas(url))
    # s_api.exl.write_xlsx(s_api.apiall_list)


    s_api.driver_quit()