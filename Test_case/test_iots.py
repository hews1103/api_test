#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2021/3/12 15:47
# @Author : 文双
# @File : test_iots.py

import allure
import pytest
from Common import DataBase
import requests
from urllib3 import encode_multipart_formdata
from Common import Request, Assert, read_excel

request = Request.Request()
assertions = Assert.Assertions()
head = {}
token_data = ''

url = 'http://192.168.0.107:8102'


def read_list(sheet_name):
    excel_list = read_excel.read_excel_sheet('./document/TMore项目iots接口.xls', sheet_name)
    ids_list = []
    for i in range(len(excel_list)):
        # 删除excel_list中每个小list的最后一个元素,并赋值给ids_pop
        ids_pop = excel_list[i].pop()
        # 将ids_pop添加到 ids_list 里面
        ids_list.append(ids_pop)
    return excel_list, ids_list


@pytest.mark.ccc
@allure.feature("获取token")
class Test_info:
    @allure.story("登录接口")
    def test_login(self):
        try:
            login_resp = request.post_request(url='https://txqa.ziyun-cloud.com' + '/idm/v2/oauth2/token',
                                              json={
                                                  "clientId": "jySbhwDvF0JtQMAyAf",
                                                  "clientSecret": "SXwrz0c1jIAxgOf7S66Y",
                                                  "grantType": "password",
                                                  "password": "654321",
                                                  "username": "文双"
                                              })
            assertions.assert_code(login_resp.status_code, 200)
            login_resp_json = login_resp.json()
            assertions.assert_in_text(login_resp_json['message'], 'Success')
        except :
            print('获取token失败')
        else:
            # 提取token
            data_token = login_resp_json['data']['accessToken']
            data_ssoId = login_resp_json['data']['ssoId']
            # 重新赋值全局变量 head\token_data
            global head
            head = {'token': data_token, 'ssoId': data_ssoId}

    # @pytest.mark.parametrize("name,device,msg", read_list('人员名称搜索')[0], ids=read_list('人员名称搜索')[1])
    # def test_personnel(self, name, device, msg):
    #     print("name is :", name, '*' * 10, '\n', "device is :", device, '*' * 10, '\n', "msg is : ", msg)


@allure.feature("Tmore接口-iots")
class Test_TM_iots:
    # gzId = 0

    # @pytest.mark.ccc
    @allure.story("测试前的数据准备")
    def test_sjjy(self):
        after_qylu_id = DataBase.mysql_select('ziyun-iot',
                                              'SELECT id FROM `t_org_route` WHERE org_hierarchy_code = "5f8a593372024fc2b7aa900918b18f3a";')

        after_zhgz_id = DataBase.mysql_select('ziyun-iot',
                                              'SELECT id FROM `t_transform_rule` WHERE rule_name in ( "test_ws自动化流程","test_ws自动化流程-修改")')

        if after_qylu_id:
            try:
                request.delete_request(url=url + '/iots-admin/route/remove-route',
                                       json={
                                           "id": after_qylu_id['id'],
                                       }, headers=head)
                print('【企业路由数据已准备】')
            except Exception as e:
                print('企业路由测试数据删除失败：', e)
        if after_zhgz_id:
            try:
                request.delete_request(url=url + '/iots-admin/transform-rule',
                                       json={
                                           "idmAppId": "a7dAceBXjKZOEfiFpx",
                                           "transformRuleId": after_zhgz_id['id']
                                       }, headers=head)
                print('【转换规则数据已准备】')
            except Exception as e:
                print('转换规则测试数据删除失败：', e)

    @allure.story("企业路由-测试连接")
    @pytest.mark.parametrize(
        "routePort,hierarchyCode,routeTarget,routeAddress,databaseName,tableName,userName,password,msg",
        read_list('企业路由-测试连接')[0], ids=read_list('企业路由-测试连接')[1])
    def test_cslj(self, routePort, hierarchyCode, routeTarget, routeAddress, databaseName, tableName, userName,
                  password, msg):
        rp_resp = request.post_request(url=url + '/iots-admin/route/connect',
                                       json={
                                           "routePort": routePort,
                                           "hierarchyCode": hierarchyCode,
                                           "routeTarget": routeTarget,
                                           "routeAddress": routeAddress,
                                           "databaseName": databaseName,
                                           "tableName": tableName,
                                           "userName": userName,
                                           "password": password
                                       }, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    @allure.story("企业路由-新建")
    @pytest.mark.parametrize(
        "routePort,hierarchyCode,routeTarget,routeAddress,databaseName,tableName,userName,password,msg",
        read_list('企业路由-新建')[0], ids=read_list('企业路由-新建')[1])
    def test_xjly(self, routePort, hierarchyCode, routeTarget, routeAddress, databaseName, tableName, userName,
                  password, msg):
        rp_resp = request.post_request(url=url + '/iots-admin/route/add',
                                       json={
                                           "routePort": routePort,
                                           "hierarchyCode": hierarchyCode,
                                           "routeTarget": routeTarget,
                                           "routeAddress": routeAddress,
                                           "databaseName": databaseName,
                                           "tableName": tableName,
                                           "userName": userName,
                                           "password": password
                                       }, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    @allure.story("企业路由-查询")
    @pytest.mark.parametrize(
        "pageNum,pageSize,hierarchyCode,msg",
        read_list('企业路由-查询')[0], ids=read_list('企业路由-查询')[1])
    def test_cxly(self, pageNum, pageSize, hierarchyCode, msg):
        rp_resp = request.post_request(url=url + '/iots-admin/route/list',
                                       json={
                                           "pageNum": pageNum,
                                           "pageSize": pageSize,
                                           "hierarchyCode": hierarchyCode}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    # 获取orgRouteId
    @allure.story("企业路由-查询-获取路由id")
    def test_data_ly(self):
        rp_resp = request.post_request(url=url + '/iots-admin/route/list',
                                       json={
                                           "pageNum": 1,
                                           "pageSize": 10,
                                           "hierarchyCode": '5f8a593372024fc2b7aa900918b18f3a'}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        data_orgRouteId = rp_resp_json['data']['list'][0]['orgRouteId']
        return data_orgRouteId

    @pytest.mark.parametrize(
        "routePort,hierarchyCode,routeTarget,routeAddress,databaseName,tableName,userName,password,msg",
        read_list('企业路由-编辑')[0], ids=read_list('企业路由-编辑')[1])
    @allure.story("企业路由-编辑")
    def test_bjly(self, routePort, hierarchyCode, routeTarget, routeAddress, databaseName, tableName, userName,
                  password, msg):
        rp_resp = requests.put(url + '/iots-admin/route/update',
                               json={
                                   "orgRouteId": Test_TM_iots().test_data_ly(),
                                   "routePort": routePort,
                                   "hierarchyCode": hierarchyCode,
                                   "routeTarget": routeTarget,
                                   "routeAddress": routeAddress,
                                   "databaseName": databaseName,
                                   "tableName": tableName,
                                   "userName": userName,
                                   "password": password},
                               headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    # 补充场景
    @allure.story("企业路由-编辑-不存在的路由")
    def test_bjly_1(self):
        rp_resp = requests.put(url + '/iots-admin/route/update',
                               json={
                                   "orgRouteId": -9999,
                                   "routePort": 27117,
                                   "hierarchyCode": '5f8a593372024fc2b7aa900918b18f3a',
                                   "routeTarget": 'mongo',
                                   "routeAddress": '192.168.0.175',
                                   "databaseName": 'ziyun-iot',
                                   "tableName": 'test03',
                                   "userName": '',
                                   "password": ''},
                               headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], '企业路由未找到！')

    @allure.story("企业路由-查看-正常")
    def test_ckly(self):
        rp_resp = request.get_request(url=url + '/iots-admin/route/details',
                                      params={'orgRouteId': Test_TM_iots().test_data_ly()}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    # 补充场景
    @pytest.mark.parametrize("orgRouteId,msg", read_list('企业路由-查看')[0], ids=read_list('企业路由-查看')[1])
    @allure.story("企业路由-查看")
    def test_ckly(self, orgRouteId, msg):
        rp_resp = request.get_request(url=url + '/iots-admin/route/details',
                                      params={'orgRouteId': orgRouteId}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    @pytest.mark.parametrize(
        "routePort,hierarchyCode,routeTarget,routeAddress,databaseName,tableName,userName,password,msg",
        read_list('企业路由-编辑-iot库已删除的')[0], ids=read_list('企业路由-编辑-iot库已删除的')[1])
    @allure.story("企业路由-编辑-iot库已删除的")
    def test_bjly_iotdel(self, routePort, hierarchyCode, routeTarget, routeAddress, databaseName, tableName, userName,
                         password, msg):
        rp_resp = requests.put(url + '/iots-admin/route/update/no/exist',
                               json={
                                   "orgRouteId": 422,
                                   "routePort": routePort,
                                   "hierarchyCode": hierarchyCode,
                                   "routeTarget": routeTarget,
                                   "routeAddress": routeAddress,
                                   "databaseName": databaseName,
                                   "tableName": tableName,
                                   "userName": userName,
                                   "password": password},
                               headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    @allure.story("企业路由-删除-正常")
    def test_del_ly1(self):
        rp_resp = request.delete_request(url=url + '/iots-admin/route/remove-route',
                                         json={
                                             "id": Test_TM_iots().test_data_ly(),
                                         }, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    # 补充场景
    @pytest.mark.parametrize("id,msg", read_list('企业路由-删除')[0], ids=read_list('企业路由-删除')[1])
    @allure.story("企业路由-删除")
    def test_del_ly(self, id, msg):
        rp_resp = request.delete_request(url=url + '/iots-admin/route/remove-route',
                                         json={
                                             "id": id,
                                         }, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    @pytest.mark.parametrize(
        "idmAppId,ruleName,ruleTypeId,ruleDesc,state,testState,language,scriptText,testData,scriptFunName,msg",
        read_list('转换规则-新建')[0], ids=read_list('转换规则-新建')[1])
    @allure.story("转换规则-新建")
    def test_zhgz_xj(self, idmAppId, ruleName, ruleTypeId, ruleDesc, state, testState, language, scriptText, testData,
                     scriptFunName, msg):
        rp_resp = requests.post(url + '/iots-admin/transform-rule',
                                json={
                                    "idmAppId": idmAppId,
                                    "ruleName": ruleName,
                                    "ruleTypeId": ruleTypeId,
                                    "ruleDesc": ruleDesc,
                                    "state": state,
                                    "testState": testState,
                                    "language": language,
                                    "scriptText": scriptText,
                                    "testData": testData,
                                    "scriptFunName": scriptFunName},
                                headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)
        data_gzId = rp_resp_json['data']
        global gzId
        gzId = int(data_gzId)

    @pytest.mark.parametrize(
        "idmAppId,relateType,collectorVersionIdList,msg",
        read_list('转换规则-关联程序')[0], ids=read_list('转换规则-关联程序')[1])
    @allure.story("转换规则-关联程序")
    def test_zhgz_glcx(self, idmAppId, relateType, collectorVersionIdList, msg):
        rp_resp = requests.put(url + '/iots-admin/transform-rule/cvs',
                               json={
                                   "idmAppId": idmAppId,
                                   "transformRuleId": gzId,
                                   "relateType": relateType,
                                   "collectorVersionIdList": [collectorVersionIdList]
                               },
                               headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    @pytest.mark.parametrize(
        "idmAppId,ruleName,ruleDesc,msg", read_list('转换规则-修改')[0], ids=read_list('转换规则-修改')[1])
    @allure.story("转换规则-修改")
    def test_zhgz_xg(self, idmAppId, ruleName, ruleDesc, msg):
        rp_resp = requests.patch(url + '/iots-admin/transform-rule',
                                 json={
                                     "id": gzId,
                                     "idmAppId": idmAppId,
                                     "ruleName": ruleName,
                                     "ruleDesc": ruleDesc
                                 },
                                 headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    @pytest.mark.parametrize(
        "idmAppId,msg", read_list('转换规则-删除')[0], ids=read_list('转换规则-删除')[1])
    @allure.story("转换规则-删除")
    def test_zhgz_del(self, idmAppId, msg):
        rp_resp = request.delete_request(url=url + '/iots-admin/transform-rule',
                                         json={
                                             "idmAppId": idmAppId,
                                             "transformRuleId": gzId
                                         }, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)
