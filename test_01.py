#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2021/3/12 18:14
# @Author : 文双
# @File : test_01.py

import allure
import pytest
from Common import DataBase
import requests
from urllib3 import encode_multipart_formdata
from Common import Request, Assert, read_excel

request = Request.Request()

def test_sjjy():
    after_qylu_id = DataBase.mysql_select('ziyun-iot',
                                          'SELECT id FROM `t_org_route` WHERE org_hierarchy_code = "5f8a593372024fc2b7aa900918b18f3a";')

    after_zhgz_id = DataBase.mysql_select('ziyun-iot',
                                          'SELECT id FROM `t_transform_rule` WHERE rule_name in ( "test_ws自动化流程","test_ws自动化流程-修改")')


    print(after_zhgz_id,after_qylu_id)

def test_01():
    request.delete_request(url='www.baidu.com',json={'data':1})
