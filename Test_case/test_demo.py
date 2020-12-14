import allure
import pytest
import json
import requests
from Common import DataBase
from Common import Request, Assert, read_excel
from urllib3 import encode_multipart_formdata

request = Request.Request()
assertions = Assert.Assertions()
head = {}
token_data = ''
url = 'https://txqa.ziyun-cloud.com'

excel_list = read_excel.read_excel_sheet('./document/回归用例.xls', 'DNC系统')
ids_list = []
for i in range(len(excel_list)):
    # 删除excel_list中每个小list的最后一个元素,并赋值给ids_pop
    ids_pop = excel_list[i].pop()
    # 将ids_pop添加到 ids_list 里面
    ids_list.append(ids_pop)


@pytest.mark.ddd
@allure.feature("回归测试")
@allure.issue("https://txqa.ziyun-cloud.com")
class Test_info:
    @allure.severity("blocker")
    @allure.story("用户登录")
    @allure.testcase("https://txqa.ziyun-cloud.com/factoryPortal/login", name="正常登录")
    def test_login(self):
        login_resp = request.post_request(url='https://txqa.ziyun-cloud.com' + '/factoryPortal/login',
                                          json={"ssoId": "柒柒", "password": "123456", "userType": ""})
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')
        # 提取token
        data_token = login_resp_json['data']['token']
        # 重新赋值全局变量 head\token_data
        global head
        global token_data
        token_data = data_token
        head = {'token': token_data}
        print(token_data)

    @pytest.mark.parametrize('ff,address,data,key,sql_data,excel_file,msg', excel_list, ids=ids_list)
    @allure.story("回归用例")
    def test_personnel(self, ff, address, data, key, sql_data, excel_file, msg):
        rp_resp = ''
        #去除接口地址中的空格
        address = address.replace(" ", '')
        #去除上传文件路径中的空格
        excel_file = excel_file.replace(" ", '')
        #sql为空或不填
        if sql_data is None or sql_data == '':
            if ff == 'get':
                rp_resp = request.get_request(url=url + address,
                                              params=data, headers=head)
            elif ff == 'post' and excel_file is None or excel_file == '':
                rp_resp = request.post_request(url=url + address,
                                               json=json.loads(data), headers=head)
            elif ff == 'post' and excel_file is not None or excel_file != '':
                with open(str(excel_file), mode="r", encoding="utf-8")as f:
                    file_splist = excel_file.split("/")
                    data_splist = data.split(":")
                    data2_splist = data_splist[1].split(",")
                    file = {"file": (file_splist[-1], f.read()), data_splist[0]: data2_splist[0],
                            data2_splist[1]: data_splist[2]}
                    encode_data = encode_multipart_formdata(file)
                    file_data = encode_data[0]
                    headers_from_data = {"Content-Type": encode_data[1],
                                         "token": token_data}
                rp_resp = request.post_request(url=url + address,
                                               data=file_data, headers=headers_from_data)
            elif ff == 'put':
                rp_resp = requests.put(url + address,
                                       json=json.loads(data), headers=head)
            #执行断言
            assertions.assert_code(rp_resp.status_code, 200)
            rp_resp_json = rp_resp.json()
            assertions.assert_in_text(rp_resp_json['message'], msg)
        elif sql_data is not None or sql_data != '':
            split = sql_data.split(",", 1)
            db_ = str(split[0])
            sql_ = str(split[1])
            if ff == 'get':
                select_data = DataBase.mysql_select_hg(db=db_, sql=sql_)
                ver = ''
                for j in select_data:
                    ver = select_data[j]
                all_data = "{}={}".format(key, ver)
                rp_resp = request.get_request(url=url + address,
                                              params=data + all_data, headers=head)
            if ff == 'post':
                select_data = DataBase.mysql_select_hg(db=db_, sql=sql_)
                v = 0
                for i in select_data:
                    v1 = select_data[i]
                    v = v1
                v_data = {key: v}
                rp_resp = request.post_request(url=url + address,
                                               json={**json.loads(data), **v_data}, headers=head)
            if ff == 'put':
                select_data = DataBase.mysql_select_hg(db=db_, sql=sql_)
                v = 0
                for i in select_data:
                    v1 = select_data[i]
                    v = v1
                v_data = {key: v}
                rp_resp = requests.put(url + address,
                                       json={**json.loads(data), **v_data}, headers=head)
            #执行断言
            assertions.assert_code(rp_resp.status_code, 200)
            rp_resp_json = rp_resp.json()
            assertions.assert_in_text(rp_resp_json['message'], msg)
