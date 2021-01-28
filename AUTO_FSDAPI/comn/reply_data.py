#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/26 10:02
__Author__=
__Des__=
"""
import jsonpath
from comn.log import Log
from comn.oper_excel import Oper_Excel
import json

class Handle_replydata(object):

    def __init__(self):
        self.log=Log()
        self.excel=Oper_Excel("fsd_api.xlsx")

    def get_cases(self):
        '''
        用例data
        :return:
        '''
        return self.excel.get_cases()

    def get_reply_value(self,replyparams,datas,relykeys):
        '''
        根据用例依赖关系参数获取依赖值
        :param replyparams: 依赖关系参数
        :return: 返回依赖值
        '''

        try:
            reply_values = []
            for replyparam in replyparams.split(";"):
                li_replyparam=replyparam.replace("\n","").split("->")
                if len(li_replyparam) > 0:
                    caseid, keyspath = li_replyparam
                    response_data=self.excel.get_cell_value(self.excel.get_row_index("A", caseid), 15)
                    reply_values.append(jsonpath.jsonpath(json.loads(response_data),keyspath)[0])

            for num,relykey in enumerate(relykeys.split(",")):
                if isinstance(datas[relykey], list):
                    list1=[]
                    list1.append(reply_values[num])
                    datas[relykey]=list1
                elif isinstance(datas[relykey], str):
                    datas[relykey]=str(reply_values[num])
                else:
                    datas[relykey]=reply_values[num]
            return datas

        except Exception as e:
            self.log.logger.error("前置条件{},异常{}".format(replyparams, e))

    def set_cellvalue(self,caseid,datas,type=1):
        '''
        将依赖数据或响应数据写入excel表格
        :param caseid:
        :param datas:
        :param type:1表示请求数据，2表示响应数据
        :return:
        '''
        try:
            if isinstance(datas,dict):
                datas=json.dumps(datas, indent=4, ensure_ascii=False)
            rowindx=self.excel.get_row_index("A",caseid)
            if type==1:
                self.excel.set_cell_value(row=rowindx,col=8,value=datas)
            elif type==2:
                self.excel.set_cell_value(row=rowindx,col=15,value=datas)
        except Exception as e:
            self.log.logger.error("表格写入报错".format(e))




if __name__ == '__main__':
    # replyparams="FSD0003->$.infoData.list[0].id;FSD0011->$.infoData.list[0].userId"
    # for replyparam in replyparams.split(";"):
    #     if len(replyparam.split("->"))>0:
    #         caseid, keyspath=replyparam.split("->")
    #         print(caseid,keyspath)

    replydata=Handle_replydata()
    datas =json.loads(replydata.excel.get_cell_value(replydata.excel.get_row_index("A", "FSD0013"), 15))
    print("+++++++++++++",datas)

    keys_path = "$.infoData.list[(@.length-1)].id"
    # keys_path = "$..list.length()"

    print(jsonpath.jsonpath(datas, keys_path))
