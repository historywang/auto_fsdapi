#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/19 14:06
__Author__=
__Des__=
"""

import allure,pytest
import os

if __name__ == '__main__':
    pytest.main(['-s','./','--alluredir','temp'])
    os.system('allure generate ./temp -o ./report --clean')