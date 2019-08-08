#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: testConnection.py
@time: 2019/8/6 14:40
@function:通过给的连接参数测试是否能够连接上数据库，失败返回False和错误对象msg，成功返回True和游标cursor
@inputParam 用户名 密码 链接 服务名
@returnParam 状态值+错误对象或连接对象
'''
import cx_Oracle

def connectOracle(userName, passWord, host, serviceName):
    try:
        connection=cx_Oracle.connect(userName, passWord, host + "/" + serviceName)
    except cx_Oracle.DatabaseError as msg:
        return False,msg
    return True,connection
