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



"""
      增加一条新备份信息
"""
def insertCurrentContrast(backupVersion,backupTime,beginTime,endTime):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = 'INSERT INTO backupInformation VALUES(5,"%s","%s","%s","%s",1);'%(backupVersion,backupTime,beginTime,endTime)
    sqlite3Cursor.execute(sql)

    sqlite3Conn.close()

insertCurrentContrast('v101','190808','190704','190801')
