#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/15 15:15
__Author__=
__Des__=
"""

from configparser import ConfigParser
from comn.init_path import Conf_fp



class Configure(ConfigParser):
    """
    获取配置文件信息
    """
    # session:
    S_BASECONF = 'baseconf'
    #option
    O_HOST = 'host'
    O_NAME='username'
    O_PWD='password'
    O_GRANT_TYPE='password'
    O_AUTHORIZATION='Authorization'
    def __init__(self):
        '''
        初始化数据，包括测试地址，登录的用户名和密码等等
        '''
        super().__init__()
        #读取配置文件
        super().read(Conf_fp,encoding='utf-8')
        #测试地址
        self.HOST=self.get_confvalue(Configure.S_BASECONF, Configure.O_HOST)
        #登录用户名
        self.NAME=self.get_confvalue(Configure.S_BASECONF, Configure.O_NAME)
        #登录密码
        self.PWD=self.get_confvalue(Configure.S_BASECONF, Configure.O_PWD)
        #授权方式
        self.GRANT_TYPE=self.get_confvalue(Configure.S_BASECONF, Configure.O_GRANT_TYPE)
        #授权
        self.AUTHORIZATION=self.get_confvalue(Configure.S_BASECONF, Configure.O_AUTHORIZATION)




    def get_confvalue(self,section,option):
        '''
        读取配置文件中的值
        :param section:
        :param option:
        :return:
        '''
        return super().get(section,option)

    def set_confvalue(self,section,option,value):
        '''
        设置配置列表中的值，类似下拉列表
        :param section:
        :param option:
        :param value:
        :return:
        '''
        if not super().has_section(section):
            super().add_section(section)
        super().set(section, option, value)
        with open(Conf_fp,'w+',encoding='utf-8') as f:
            super().write(f)




if __name__ == '__main__':
    conf=Configure()
    print(conf.HOST)
    conf.set_confvalue("nihao","xiexie","hello")