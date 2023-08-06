#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@File Name  : learn_unittest
@Author     : LeeCQ
@Date-Time  : 2021/1/10 0:04
"""
import unittest

if __name__ == '__main__':
    # 第一种加载方式：
    # unittest.main()
    # 第二种加载方式：
    # 构建测试套件：将要执行的测试用例添加到测试套件里
    suite = unittest.TestSuite()
    suite.addTest(TestAdd("test_add1"))
    suite.addTest(TestSub("test_sub1"))
    suite.addTest(TestSub("test_sub2"))
    suite.addTest(TestAdd("test_add2"))
    # 通过测试运行器执行测试套件
    runner = unittest.TextTestRunner()
    runner.run(suite)

    # 使用unitest提供的discover方法自动发现测试用例

    # 定义测试用例的目录
    # test_dir='./'
    # #使用discover方法去发现测试用例放到discover里
    # discover=unittest.defaultTestLoader.discover(test_dir,pattern='test*.py')
    # #使用测试运行器去执行加载在discover里的测试用例
    # runner=unittest.TextTestRunner()
    # runner.run(discover)
