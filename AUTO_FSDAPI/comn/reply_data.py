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
    '''
    获取所有测试用例数据
    get_cases() 获取所有用例data
    get_reply_value 依据case依赖获取数据
    '''

    def __init__(self):
        self.log=Log()
        self.excel=Oper_Excel("fsd_api.xlsx")

    def get_cases(self):
        '''
        获取所有用例data
        :return:
        '''
        return self.excel.get_cases()

    def get_reply_value(self,replyparams,datas,relykeys):
        '''
        根据用例依赖关系参数获取依赖值,并写入到excel表格
        支持多接口依赖
        例如：依赖关系参数
            FSD0003->$.infoData.list[0].id;
            FSD0011->$.infoData.list[0].userId;
            FSD0014->$.infoData.list[(@.length-1)].networkUUID

            通过；号分隔，表示依赖那几个用例
            FSD0003 表示用例编号
            $.infoData.list[0].id 要获取的依赖数据的json路径
                jsonpath.jsonpath(json.loads(response_data),keyspath)
                jsonpath.jsonpath返回的数据是个列表类型，根据需要取值
                例如，批量操作，选取多个值时，如果需要传递参数为数组时，直接取值
                     【【参见：删除用户 请求参数userIds是数组】】
                     批量操作，选取多个值时，如果需要传递值为一个字符串集，需要先将获取的列表转换为str字符串
                     【【参见：创建云桌面，选取多个用户 请求参数userIds是由多个userid拼成的字符串】】
                     其他操作，直接赋值即可。
        :param replyparams: 依赖关系参数
        :param datas: 请求参数
        :param relykeys: 依赖键值
        :return: 返回请求参数
        '''

        try:
            reply_values = []
            for replyparam in replyparams.split(";"):
                li_replyparam=replyparam.replace("\n","").split("->")
                if len(li_replyparam) > 0:
                    caseid, keyspath = li_replyparam
                    #获取写入excel表格中的响应数据，对应response_data
                    response_data=self.excel.get_cell_value(self.excel.get_row_index("A", caseid), 14)
                    #获取依赖数据
                    getvalues=jsonpath.jsonpath(json.loads(response_data), keyspath)
                    #根据需要将依赖数据加到reply_values列表中
                    if len(getvalues)>1:
                        reply_values.append(getvalues)
                    else:
                        reply_values.append(getvalues[0])

            for num,relykey in enumerate(relykeys.split(",")):
                #判断参数类型，是列表数组或其他
                if isinstance(datas[relykey], list):
                    list1=[]
                    list1.append(reply_values[num])
                    datas[relykey]=list1
                elif isinstance(datas[relykey], str):
                    #先判断是否是个列表类型，并且长度大于1
                    if isinstance(reply_values[num], list) and len(reply_values[num])>1:
                        #此处将列表转换成字符串，考虑到会传递int组合的列表
                        datas[relykey]= (",").join([str(i) for i in reply_values[num]])
                    else:
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
                #第8列为请求参数列，datas
                self.excel.set_cell_value(row=rowindx,col=8,value=datas)
            elif type==2:
                # 第14列为响应数据列，response_data
                self.excel.set_cell_value(row=rowindx,col=14,value=datas)
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
    # print("+++++++++++++",datas)

    # keys_path = "$.infoData.list[(@.length-1)].[id,path]"
    keys_path = "$.infoData.list[0,1].id"

    # keys_path = "$..list.length()"

    listt=jsonpath.jsonpath(datas, keys_path)
    if len(listt)>1:
        print((",").join([str(i) for i in listt]))


