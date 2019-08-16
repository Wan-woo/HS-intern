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
import sqlite3
import backGround.globalConn as gC

def connectOracle(userName, passWord, host, serviceName):
    try:
        connection=cx_Oracle.connect(userName, passWord, host + "/" + serviceName)
    except cx_Oracle.DatabaseError as msg:
        return False, str(msg)
    gC._init()
    gC.set_value('userName', userName)
    gC.set_value('passWord', passWord)
    gC.set_value('host', host)
    gC.set_value('serviceName', serviceName)
    return True

def getOrcaleConnection():
    gC._init()
    userName = gC.get_value('userName')
    passWord = gC.get_value('passWord')
    host = gC.get_value('host')
    serviceName = gC.get_value('serviceName')
    try:
        connection=cx_Oracle.connect(userName, passWord, host + "/" + serviceName)
        return connection
    except cx_Oracle.DatabaseError as msg:
        print(msg)
        return -1
def getSqliteConnection():

    try:
        connection=sqlite3.connect("test.db")
        return connection
    except cx_Oracle.DatabaseError as msg:
        print(msg)
        return -1
# 测试语句 第一条正常 第二条报错
# print(connectOracle('faisdb','faisdb','192.168.36.244','fais'))
# print(connectOracle('faisdb','faisdb','192.168.36.244','fais1'))
