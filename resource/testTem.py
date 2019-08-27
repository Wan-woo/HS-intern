#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: testTem.py
@time: 2019/8/7 14:18
@function:
@inputParam:
@returnParam:
'''
# from getBackupInfo import getBackupInfo
# testList = getBackupInfo()
# print(testList)
#11111


import logging
def myLogging():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
    fp = logging.FileHandler('log.txt', encoding='utf-8')
    fs = logging.StreamHandler()
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])    # 调用
    return logging

    # logging.debug("This is a debug log.哈哈")
    # logging.info("This is a info log.")
    # logging.warning("This is a warning log.")
    # logging.error("This is a error log.")
    # logging.critical("This is a critical log.")
