#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: getBackupInfo.py
@time: 2019/8/6 14:54
@function:查询备份的信息
@inputParam:
@returnParam:
'''
import sqlite3




# print(getBackupTime('1'))





"""
        通过功能与指标名查询对象
    :type 1.function 功能 2.Quota 指标
"""
def getObjectByModule(FunctionQuotaName,typeCode):
    if(typeCode!=1&typeCode!=2):
        print("参数不合法")
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "SELECT * FROM moduleObject WHERE functionQuotaType ="+str(typeCode)+"AND functionQuotaName = "+FunctionQuotaName+""
    sqlite3Cursor.execute(sql)
    objectInfo = sqlite3Cursor.fetchall()
    sqlite3Conn.close()
    return objectInfo













# print(getFunctionQuotaInfo())
# print(getMoudleInfo())
# print(getBackupInfo())
# print(getbackupObjectId())

