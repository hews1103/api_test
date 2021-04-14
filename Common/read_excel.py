import xlrd
import sys


def read_excel_sheet(file, sheet_name):
    li = []
    wb = xlrd.open_workbook(filename=file)  # 打开文件
    # print(wb.sheet_names())  # 打印所有表格名字
    sheet_names = wb.sheet_names()  # 获取所有工作表名称
    # 判断输入表名是否实际存在于excel内
    if sheet_name not in sheet_names:
        print('ERROR!!!\n输入表名错误，输入表名为：{}。存在的表名有{}'.format(sheet_name, sheet_names))
        sys.exit()
    sheet_data = wb.sheet_by_name(sheet_name)  # 通过工作表名称获取某张表格
    # 获取表格内从第二行到最后一行的数据
    for i in range(1, sheet_data.nrows):
        # l.append(sheet1.row_values(i))
        d = tuple()
        for j in range(sheet_data.ncols):
            d = sheet_data.row_values(i)
        li.append(d)

    # print(l)
    return li
