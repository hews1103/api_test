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

url = 'https://txqa.ziyun-cloud.com/dnc'

excel_list = read_excel.read_excel_sheet('./document/DNC系统.xls', '人员名称搜索')
ids_list = []
for i in range(len(excel_list)):
    # 删除excel_list中每个小list的最后一个元素,并赋值给ids_pop
    ids_pop = excel_list[i].pop()
    # 将ids_pop添加到 ids_list 里面
    ids_list.append(ids_pop)


@allure.feature("获取potal端登录用户信息")
class Test_info:
    @pytest.mark.ccc
    @allure.story("用户登录接口")
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
        print(head)


deviceId = "7429"
fileId = 172
versionId = 378
# name = "王富贵"
recycleId = 0
recycleIds = 0
fileIds = 172


@allure.feature("设备目录分发页、回传页接口")
class Test_device_ml:
    @pytest.mark.ccc
    @allure.story("上传文件")
    def test_scwj(self):
        select_data = DataBase.mysql_select(db='ziyun-iot', sql='SELECT * FROM `t_device` where device_id ="7429";',
                                            attribute='cnc_brand')
        a = 0
        while a < 2:
            if select_data == 'Fanuc':
                with open('./document/FLK_0.nc', mode="r", encoding="utf-8")as f:
                    file = {"file": ('FLK_0.nc', f.read()), "deviceId": deviceId, "remark": "自动化备注"}
                    encode_data = encode_multipart_formdata(file)
                    file_data = encode_data[0]
                    headers_from_data = {"Content-Type": encode_data[1],
                                         "token": token_data}

                rp_resp = request.post_request(url=url + '/file/upload',
                                               data=file_data, headers=headers_from_data)
                assertions.assert_code(rp_resp.status_code, 200)
                login_resp_json = rp_resp.json()
                assertions.assert_in_text(login_resp_json['message'], 'Success')
                a += 1
            elif select_data == 'Siemens':
                with open('./document/XMZ_0.txt', mode="r", encoding="utf-8")as f:
                    file = {"file": ('XMZ_0.txt', f.read()), "deviceId": deviceId, "remark": "自动化备注"}
                    encode_data = encode_multipart_formdata(file)
                    file_data = encode_data[0]
                    headers_from_data = {"Content-Type": encode_data[1],
                                         "token": token_data}

                rp_resp = request.post_request(url=url + '/file/upload',
                                               data=file_data, headers=headers_from_data)
                assertions.assert_code(rp_resp.status_code, 200)
                login_resp_json = rp_resp.json()
                assertions.assert_in_text(login_resp_json['message'], 'Success')
                a += 1

    @allure.story("文件列表")
    def test_file_list(self):
        rp_resp = request.get_request(url=url + '/file/list',
                                      params={'pageSize': 10, 'pageNum': 1, 'type': 0, 'deviceId': deviceId},
                                      headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        rp_fileid = str(rp_resp_json['data']['list'][0]['fileId'])
        global fileId
        fileId = rp_fileid
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    @allure.story("下载文件/预览文件内容")
    def test_download(self):
        rp_resp = request.get_request(url=url + '/file',
                                      params={'fileId': fileId},
                                      headers=head)
        assertions.assert_code(rp_resp.status_code, 200)

        assertions.assert_in_text(rp_resp.text, '%')

    @allure.story("查询历史信息")
    def test_history_list(self):
        rp_resp = request.get_request(url=url + '/file/list/history',
                                      params={'fileId': fileId, 'type': 0}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        rp_versionid = rp_resp_json['data'][0]['versionId']
        global versionId
        versionId = rp_versionid
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    @allure.story("历史版本文件下载")
    def test_history_download(self):
        rp_resp = request.get_request(url=url + '/file/version',
                                      params={'versionId': versionId},
                                      headers=head)
        assertions.assert_code(rp_resp.status_code, 200)

        assertions.assert_in_text(rp_resp.text, '%')

    @allure.story("上传文件前的校验")
    def test_wjjy(self):
        rp_resp = request.post_request(url=url + '/file/upload/check',
                                       json={"fileListName": ["为空文件.txt"], "deviceId": deviceId}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    @allure.story("修改备注")
    def test_xgbz(self):
        rp_resp = requests.put(url + '/file/edit/remark',
                               json={'versionId': versionId, 'remark': "自动化编辑备注"}, headers={'token': token_data})
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    @pytest.mark.parametrize('name,device,msg', excel_list, ids=ids_list)
    @allure.story("人员名称搜索")
    def test_personnel(self, name, device, msg):
        rp_resp = request.get_request(url=url + '/file/blurry/user',
                                      params={'name': name, 'deviceId': device}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], msg)

    @allure.story("文件回滚")
    def test_file_hg(self):
        rp_resp = requests.put(url + '/rollback',
                               json={'fileId': fileId, 'versionId': versionId, 'reason': '自动化回滚'},
                               headers={'token': token_data})
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        print(rp_resp_json)
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    @allure.story("文件删除到回收站")
    def test_delete_cache(self):
        rp_resp = requests.put(url + '/file/delete',
                               json={'reason': '自动化删除', 'fileId': fileId}, headers={'token': token_data})
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    @allure.story("回收站查询列表")
    def test_hszcxlb(self):
        rp_resp = request.post_request(url=url + '/recycle/query/list',
                                       json={"pageNum": 1, "pageSize": 20, "type": 0}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    @allure.story("回收站列表")
    def test_hszlb(self):
        rp_resp = request.post_request(url=url + '/recycle/page/list',
                                       json={"pageNum": 1, "pageSize": 20, "type": 0}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], 'Success')
        recycle_id_ = rp_resp_json['data']['list'][0]['recycleId']
        file_ids_ = rp_resp_json['data']['list'][0]['fileId']
        global recycleId
        global fileIds
        fileIds = file_ids_
        recycleId = recycle_id_

    @allure.story("回收站还原")
    def test_hszhy(self):
        rp_resp = request.get_request(url=url + '/recycle/restore',
                                      params={'recycleId': recycleId}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], '还原成功')

    @allure.story("文件再次删除到回收站")
    def test_delete2_cache(self):
        rp_resp = requests.put(url + '/file/delete',
                               json={'reason': '二次接口删除', 'fileId': fileId}, headers={'token': token_data})
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], 'Success')

    @allure.story("回收站彻底删除")
    def test_hszsc(self):
        rp_resp = request.post_request(url=url + '/recycle/delete',
                                       json={"recycleIds": [recycleId], "fileIds": [fileIds]}, headers=head)
        assertions.assert_code(rp_resp.status_code, 200)
        rp_resp_json = rp_resp.json()
        assertions.assert_in_text(rp_resp_json['message'], '删除成功')


if __name__ == '__main__':
    ml = Test_device_ml()
    ml.test_file_hg()
