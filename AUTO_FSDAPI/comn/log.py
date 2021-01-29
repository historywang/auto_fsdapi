# -*- coding: utf-8 -*-
import logging
import logging.config
import json
from comn.init_path import Logjson_fp


class Log(object):
    # logging.basicConfig(level=logging.INFO,filename='aa.log')
    # logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s -%(filename)s - %(message)s')
    # logger=logging.getLogger(__name__)
    # logger.setLevel(level=logging.INFO)
    # #处理器写日志到指定目录位置
    # handler=logging.FileHandler('aa.txt')
    # #设置日志格式
    # formatter=logging.Formatter('%(asctime)s - %(name)s -%(filename)s - %(message)s')
    # handler.setFormatter(formatter)
    # #添加一个写日志的处理器器
    # logger.addHandler(handler)
    # logger.info('start print log')



    def __init__(self):
        #返回日志器的名称
        self.logger=logging.getLogger('apilogger')
        self.set_config()


    def set_config(self):
        '''
        设置日志格式
        :return:
        '''
        with open(Logjson_fp,'r',encoding='utf-8-sig') as f:
            config=json.load(f)
            logging.config.dictConfig(config)

if __name__ == '__main__':
    pass
    # print(Log.filename)
    # Log=Log()
    # Log.logger.info('你好1111')
    # Log.logger.debug('你好1111')
    # Log.logger.warning('你好1111')
    # Log.logger.critical('你好1111')

