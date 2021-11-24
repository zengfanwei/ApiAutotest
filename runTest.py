# C:\Users\zengf\AppData\Local\Programs\Python\Python39 python3
# -*- encoding: utf-8 -*-
# @Author : zeng fanwei
# @File : runTest.py
# @Time : 2021/11/24 15:40
# @Software : PyCharm

import time
import sys
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest


def runTest():
    # 指定测试用例为当前文件夹下的 interface 目录
    test_dir = './testcases'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './reports/' + now + '_result.html'
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(stream=fp,
                             title='Punball API AutoTest Report',
                             description='Case Result: ')
        runner.run(discover)
    fp.close()


if __name__ == "__main__":
    runTest()
