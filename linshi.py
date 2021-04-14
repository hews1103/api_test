#! /usr/bin/env python3

# eg:1
# from sys import argv, path  # 导入特定的成员
#
# print('================python from import===================================')
# print('path:',argv)  # 因为已经导入path成员，所以此处引用时不需要加sys.path

# eg :2
# import sys
#
# print('================Python import mode==========================')
# print('命令行参数为:')
# for i in sys.argv:
#     print(i[0:i.rfind('/')])
# print('\n python 路径为', sys.path)

# eg:3
# a, b, c = 1, 2, "runoob"
# print(a,b,c)

# eg:4
# class A:
#     pass
#
# class B(A):
#     pass
#
# print(type(B())==A)
# print(isinstance(B(),A))

# eg:5
# class MyNumbers:
#     def __iter__(self):
#         self.a = 1
#         return self
#
#     def __next__(self):
#         if self.a <= 20:
#             x = self.a
#             self.a += 1
#             return x
#         else:
#             raise StopIteration
#
#
# myclass = MyNumbers()
# myiter = iter(myclass)
#
# for i in myiter:
#     print(i)

# eg:6
# import sys
#
# def fibonacci(n):  # 生成器函数 - 斐波那契
#     a, b, counter = 0, 1, 0
#     while True:
#         if (counter > n):
#             return
#         yield a
#         a, b = b, a + b
#         counter += 1
#
# f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成
#
# while True:
#     try:
#         print(next(f), end=" ")
#     except StopIteration:
#         sys.exit()

# import sys,time
#
# # 加入迭代器可以减少同一时间对内存的使用率，如果是计算一万以内的乘法表用for循环就不太适用
#
# def cc(n):
#     if n <= 10000:
#         for i in range(1, n + 1):
#             for j in range(1, i + 1):
#                 print('{} * {} ='.format(j, i), i * j, end='\t\t')
#             yield
#             # print('\t')
#     else:
#         print('超出计算范围')
#
#
# f = cc(1111)
# while True:
#     try:
#         next(f)
#         print('')
#     except StopIteration:
#         sys.exit()
#     else:
#         print(time.thread_time())


# matrix =[[1,2,3],[4,5,6]]
# a = [[row[i] for row in matrix] for i in range(3)]
# print(a)

# import math
# a = '测试：{0:.3f}'.format(math.pi)
# print(a)
# table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
# print('Runoob: {Runoob:d}; Google: {Google:d}; Taobao: {Taobao:d}'.format(**table))


# class MyError(Exception):
#     def __init__(self, value):
#         self.value = value
#
#     def __str__(self):
#         return repr(self.value)
#
# try:
#     raise MyError(2 * 2)
# except MyError as e:
#     print('My exception occurred, value:', e.value)
#

# class MyClass:
#     """一个简单的类实例"""
#     i = 12345
#
#     def f(self):
#         return 'hello world'
#
#
# # 实例化类
# x = MyClass()
#
# # 访问类的属性和方法
# print("MyClass 类的属性 i 为：", x.i)
# print("MyClass 类的方法 f 输出为：", x.f())

# 类定义
# class people:
#     # 定义基本属性
#     name = ''
#     age = 0
#     # 定义私有属性,私有属性在类外部无法直接进行访问
#     __weight = 0
#
#     # 定义构造方法
#     def __init__(self, n, a, w):
#         self.name = n
#         self.age = a
#         self.__weight = w
#
#     def speak(self):
#         print("%s 说: 我 %d 岁。" % (self.name, self.age))
#
#
# # 单继承示例
# class student(people):
#     grade = ''
#
#     def __init__(self, n, a, w, g):
#         # 调用父类的构函
#         people.__init__(self, n, a, w)
#         self.grade = g
#
#     # 覆写父类的方法
#     def speak(self):
#         print("%s 说: 我 %d 岁了，我在读 %d 年级" % (self.name, self.age, self.grade))
#
#
# s = student('ken', 10, 60, 3)
# s.speak()


# class people:
#     def __init__(self,q,w,e):
#         self.name =  q
#         self.age = w
#         self.address = e
#     def speak(self):
#         print('%s 说：我%s岁了，我住在%s' %(self.name,self.age,self.address))
#
# class A(people):
#     def __init__(self,q,w,e,r):
#         people.__init__(self,q,w,e)
#         self.school = r
#     def speak(self):
#         print('%s 说：我%s岁了，我住在%s，在%s上学。' %(self.name,self.age,self.address,self.school))
#
# s = A('joe',11,'New York','shanghai')
# s.speak()

# def multiply(a, b):
#     """
#     >>> multiply(4, 3)
#     12
#     >>> multiply('a', 3)
#     'aaa'
#     """
#     return a * b
# if __name__=='__main__':
#     import doctest
#     doctest.testmod(verbose=True)

# # 引入日历模块
# import calendar
#
# # 输入指定年月
# yy = int(input("输入年份: "))
# mm = int(input("输入月份: "))
#
# # 显示日历
# print(calendar.month(yy, mm))


# # 约瑟夫生者死者小游戏
# # 30 个人在一条船上，超载，需要 15 人下船。
# #
# # 于是人们排成一队，排队的位置即为他们的编号。
# #
# # 报数，从 1 开始，数到 9 的人下船。
# #
# # 如此循环，直到船上仅剩 15 人为止，问都有哪些编号的人下船了呢？
# people = {}
# for x in range(1, 31):
#     people[x] = 1
# # print(people)
# check = 0
# i = 1
# j = 0
# while i <= 31:
#     if i == 31:
#         i = 1
#     elif j == 15:
#         break
#     else:
#         if people[i] == 0:
#             i += 1
#             continue
#         else:
#             check += 1
#             if check == 9:
#                 people[i] = 0
#                 check = 0
#                 print("{}号下船了".format(i))
#                 j += 1
#             else:
#                 i += 1
#                 continue


# !/usr/bin/env python
# -*- coding:utf-8 -*-
# print('\033[1;31;40m')     #下一目标输出背景为黑色，颜色红色高亮显示
#
# print('*' * 50)
# print('\033[7;31m错误次数超限，用户已被永久锁定，请联系管理员！\033[1;31;40m')  #字体颜色红色反白处理
# print('*' * 50)
# print('\033[0m')

# def eff(arr,i):
#     # arr = [2, 3, 4, 10, 40]
#     # i = 3
#     arr.sort()
#     if len(arr) >= 1:
#         if i in arr:
#             while True:
#                 a = int(1 + (len(arr) - 1) / 2)
#                 if arr[a] == i:
#                     print(arr[a])
#                     break
#                 elif arr[a] > i:
#                     arr = arr[0:a]
#                 else:
#                     arr = arr[a:]
#         else:
#             print('列表不存在该元素')
#     else:
#         print('列表不能为空')
# if __name__ == '__main__':
#     eff([2,3,4,56,7,12,31],31)


# import datetime
# print((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))

# # 返回 x 在 arr 中的索引，如果不存在返回 -1
# def binarySearch(arr, l, r, x):
#     # 基本判断
#     if r >= l:
#         mid = int(l + (r - l) / 2)
#         # 元素整好的中间位置
#         if arr[mid] == x:
#             return mid
#             # 元素小于中间位置的元素，只需要再比较左边的元素
#         elif arr[mid] > x:
#             return binarySearch(arr, l, mid - 1, x)
#
#             # 元素大于中间位置的元素，只需要再比较右边的元素
#         else:
#             return binarySearch(arr, mid + 1, r, x)
#     else:
#         # 不存在
#         return -1
#
# # 测试数组
# arr = [2, 3, 4, 10, 40]
# x = 11
# # 函数调用
# result = binarySearch(arr, 0, len(arr) - 1, x)
#
# if result != -1:
#     print("元素在数组中的索引为 %d" % result)
# else:
#     print("元素不在数组中")

# def test(lis,a,z,x):
#     if z>=a:
#         mid = int(a+ (z-a)/2)
#         if lis[mid] == x:
#             return mid
#         elif lis[mid]>x:
#             return test(lis,a,mid-1,x)
#         else:
#             return test(lis,mid+1,z,x)
#     else:
#         return -1
#
# lis = [2,3,4,10,12,15]
# x = 10
# res = test(lis,0,len(lis)-1,x)
# if res != -1:
#     print("元素在数组中的索引为 %d" % res)
# else:
#     print("元素不在数组中")
# s=[1,3,32]


# cc = lambda a,b,c:a-b-c
# print(cc(75067.79,72521.21,178.14))

# import _thread
# import time
#
#
# # 为线程定义一个函数
# def print_time(threadName, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print("%s: %s" % (threadName, time.ctime(time.time())))
#
#
# # 创建两个线程
# try:
#     _thread.start_new_thread(print_time, ("Thread-1", 2,))
#     _thread.start_new_thread(print_time, ("Thread-2", 4,))
# except:
#     print("Error: 无法启动线程")
#
# while 1:
#     pass


# import threading
# import time
#
# exitFlag = 0
#
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print ("开始线程：" + self.name)
#         print_time(self.name, self.counter, 5)
#         print ("退出线程：" + self.name)
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threadName.exit()
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
#
# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # 开启新线程
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print ("退出主线程")

# while True:
#     t = input("请输入一个数：")
#     s = t.strip()
#     if 0 < len(s) < 10:
#         n = int((10 - len(s)) / 2)
#         if (10 - len(s)) % 2 != 0:
#             print('*' * n, str(s), '*' * (n + 1))
#         else:
#             print('*' * n, str(s), '*' * n)
#     elif len(s) == 0:
#         print("*"*10)
#     else:
#         print(s)

# from Common import DataBase
# a = DataBase.mysql_select('ziyun-iot',
#                       'SELECT * FROM `t_org_route` WHERE org_hierarchy_code = "5f8a593372024fc2b7aa900918b18f3a";')
#
# print(a['route_port'])


# while True:
#     a=int(input("请输入"))
#
#     print('percent:{:.2%}'.format(a/855))


print(len('65432111111111111111'))