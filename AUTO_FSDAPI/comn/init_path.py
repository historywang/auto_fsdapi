#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/18 9:25
__Author__=
__Des__=
"""
import os
#获取根目录
BASHPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#获取日志配置文件目录
Logjson_fp = os.path.join(BASHPATH, "config", "logconf.json")
#获取配置文件目录
Conf_fp = os.path.join(BASHPATH, "config", "conf.ini")
#获取测试用例文件目录
TESTCASE_fp = os.path.join(BASHPATH, "test_data", "fsd_api.xlsx")
#获取要导入的用户模板文件目录
USERS_fp = os.path.join(BASHPATH, "test_data", "客户机导入模板.xlsx")


print(TESTCASE_fp)