#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/15 13:02
__Author__=
__Des__=
"""


from comn.requestapi import RequestClass
import allure,pytest,json
from comn.reply_data import Handle_replydata
from comn.asserter import Assertion
from comn.get_token import get_token

RC=RequestClass()
replycls=Handle_replydata()
asster=Assertion()
TOKEN=get_token()
class TestCase(object):
    '''
    执行测试用例
    pytest.mark.parametrize数据参数化，将所有excel表中数据做参数化处理，
    表格有几条可执行用例，就会有几条参数化数据。
    '''
    @allure.feature("FSD3.2接口测试")
    @pytest.mark.parametrize("casedatas",replycls.get_cases())
    def test_autoapi(self, casedatas):
        caseid=casedatas['caseid']
        url= casedatas['url']
        method=casedatas['method']
        content_type=casedatas.get('content-type')
        headers = {
            "Authorization": "Bearer " + TOKEN
        }
        if content_type:
            headers["content-type"] = content_type
        datas = casedatas.get('datas')
        if datas:
            datas = json.loads(datas)
        #前置条件，即用例依赖
        preconditions=casedatas.get('preconditions')
        relykeys=casedatas.get('relykey')
        if relykeys and preconditions:
            datas=replycls.get_reply_value(preconditions,datas,relykeys)
            replycls.set_cellvalue(caseid,datas,1)

        # statusMsg=casedatas['statusMsg']
        file=casedatas['file']
        dic_allure={
            "title":casedatas['casetitle'],
            "story":casedatas['casestroy'],
            "description":casedatas['description'],
            "exportfile":casedatas['exportfile']
        }
        exp_code=casedatas['exp_code']
        exp_msg=casedatas['exp_msg']
        req_code,req_txt= RC.Sendrequest(method,url=url, data=datas,headers=headers ,files=file,Content_Type=content_type,**dic_allure)
        replycls.set_cellvalue(caseid,req_txt,2)
        # asster.assert_code(req_code,exp_code)
        # asster.assert_in_body(req_txt,exp_msg)






if __name__ == '__main__':
    tc=TestCase()
    tc.test_token()