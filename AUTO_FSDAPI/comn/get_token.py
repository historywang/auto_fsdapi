#!/usr/bin/python 
# -*- coding: utf-8 -*-

"""
__title__=
__Time__= 2021/1/18 10:02
__Author__=
__Des__=
"""

from comn.conf import Configure
from comn.requestapi import RequestClass



def get_token():
    cf=Configure()
    url="permissions/uaa/oauth/token"
    datas={
        "username":cf.NAME,
        "password":cf.PWD,
        "grant_type":cf.O_GRANT_TYPE
    }
    Content_Type="application/x-www-form-urlencoded"
    headers={
        "Authorization":cf.AUTHORIZATION,
        "Content-Type":Content_Type
    }

    req_code,req_text=RequestClass().Sendrequest("post",url=url,headers=headers, data=datas,Content_Type=Content_Type,isallure=False)
    if req_code==200:
        return req_text.get("access_token")
    else:
        return ""


if __name__ == '__main__':
    print(get_token())