import pymysql.cursors
import sys

def mysql_select(db, sql, attribute):
    '''
    通过sql中的某个字段取值
    :param db:
    :param sql:
    :param attribute:
    :return:
    '''
    try:
        # 连接mysql数据库
        connection = pymysql.connect(host='MYSQL', port=3306, user='root', password='Pass1234', db=db,  # 'ziyun-dnc',
                                     cursorclass=pymysql.cursors.DictCursor)
        # 通过cursor创建游标,进行每一步操作
        cursor = connection.cursor()
        # 发起请求
        # sql = 'SELECT * FROM `app_package` where app_pk_name = "ws测试产品";'
        cursor.execute(sql)
        # 获取数据
        res = cursor.fetchone()
        # print(res)
        # 赋值变量 parm
        parm = str(res[attribute])
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        connection.close()
        # 返回参数
        return parm
    except Exception as e:
        print("ERROR!!!\n执行sql失败，将自动关闭数据库连接。\t错误信息为：{}".format(e))
        sys.exit()

def mysql_select_hg(db, sql):
    '''
    在sql中标明字段取值
    :param db:
    :param sql:
    :return:
    '''
    try:
        # 连接mysql数据库
        connection = pymysql.connect(host='MYSQL', port=3306, user='root', password='Pass1234', db=db,  # 'ziyun-dnc',
                                     cursorclass=pymysql.cursors.DictCursor)
        # 通过cursor创建游标,进行每一步操作
        cursor = connection.cursor()
        # 发起请求
        # sql = 'SELECT * FROM `app_package` where app_pk_name = "ws测试产品";'
        cursor.execute(sql)
        # 获取数据
        res = cursor.fetchone()
        # print(res)
        # 赋值变量 parm
        # parm = str(res[attribute])
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        connection.close()
        # 返回参数
        return res
    except Exception as e:
        print("ERROR!!!\n执行sql失败，将自动关闭数据库连接。\t错误信息为：{}".format(e))
        sys.exit()