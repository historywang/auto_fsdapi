#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/19 9:08
__Author__=
__Des__=
"""
from comn.log import Log
import json

class Assertion(object):
    '''
    响应断言
    '''

    def __init__(self):
        self.log=Log()

    def assert_code(self,code,exp_code):
        '''
        断言响应码，并将结果写入日志
        :param code: 实际响应码
        :param exp_code: 期望码
        :return:
        '''
        try:
            assert code==exp_code,"期望码{},实际响应码{},失败".format(exp_code,code)
        except AssertionError as e:
            self.log.logger.error(e)
            raise

    def assert_in_body(self,msg,exp_msg):
        '''
        断言期望结果是否在实际结果中
        :param msg:
        :param exp_msg:
        :return:
        '''
        try:
            msg=json.dumps(msg,ensure_ascii=False)
            assert exp_msg in msg,"实际结果{}并不包含期望内容,期望内容是{},失败".format(msg,exp_msg)
        except AssertionError as e:
            self.log.logger.error(e)
            raise

    def assert_msg(self, msg, exp_msg):
        '''
        断言期望结果和实际结果相同
        :param msg:
        :param exp_msg:
        :return:
        '''
        try:
            assert exp_msg==msg, "实际结果{}并不包含期望内容,期望内容是{},失败".format(msg, exp_msg)
        except AssertionError as e:
            self.log.logger.error(e)
            raise

    def assert_bodykey(self, body,key, exp_msg):
        '''
        断言实际结果等于相应结果
        :param body:实际结果
        :param key:键值
        :param exp_msg:相应结果
        :return:
        '''
        try:
            assert body[key]==exp_msg, "实际结果{}不等于期望内容,期望内容是{},失败".format(body[key], exp_msg)
        except AssertionError as e:
            self.log.logger.error(e)
            raise


if __name__ == '__main__':
    ast=Assertion()
    ast.assert_code(200,200)