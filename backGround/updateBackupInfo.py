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
      获得当前对比的备份
"""
def updateCurrentContrast(backupVersion):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sqlite3Cursor.execute("UPDATE backupInformation SET hasContrast == 0 ;")
    sql = "UPDATE backupInformation SET hasContrast == 0 where backupVersion = "+backupVersion+";"
    sqlite3Cursor.execute(sql)
    sqlite3Conn.close()
print(updateCurrentContrast(1))
"""
      获得当前对比的备份
"""
def updateCurrentContrast(backupVersion):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sqlite3Cursor.execute("UPDATE backupInformation SET hasContrast == 0 ;")
    sql = "UPDATE backupInformation SET hasContrast == 0 where backupVersion = "+backupVersion+";"
    sqlite3Cursor.execute(sql)
    sqlite3Conn.close()


