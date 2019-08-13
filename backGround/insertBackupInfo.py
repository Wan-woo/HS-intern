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
def insertBackupInformation(backupVersion,backupTime,beginTime,endTime):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "INSERT INTO backupInformation(backupVersion,backupTime,beginTime,endTime,hasContrast) VALUES('%d',%d,%d,%d,0);"%(backupVersion,backupTime,beginTime,endTime)
    sqlite3Cursor.execute(sql)
    sqlite3Cursor.close()
    sqlite3Conn.commit()
    sqlite3Conn.close()
"""
增加新的对象(表 存储过程)和版本
"""
def insertBackupObject(backupVersion,objectName,backupObjectName,ObjectType):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "INSERT INTO backupObjectNameList(backupVersion,objectName,backupObjectName,ObjectType) VALUES('%s','%s','%s','%s');"%(backupVersion,objectName,backupObjectName,ObjectType)
    sqlite3Cursor.execute(sql)
    sqlite3Cursor.close()
    sqlite3Conn.commit()
    sqlite3Conn.close()
"""
      增加一条新模块信息
"""
def insertMoudleList(moudleName):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "INSERT INTO moudleList(moudleName,isSystemDefineModule) VALUES('%s','%s');"%(moudleName,0)
    sqlite3Cursor.execute(sql)
    sqlite3Cursor.close()
    sqlite3Conn.commit()
    sqlite3Conn.close()

"""
      增加一条模块与对象对应关系
"""
def insertMoudleObject(moudleName,objectName,objectType,isSystemDefine):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "INSERT INTO moudleObject(moudleName,objectName,objectType,isSystemDefine) VALUES('%s','%s','%s','%s','%s');"%(moudleName,objectName,objectType,isSystemDefine,0)
    sqlite3Cursor.execute(sql)
    sqlite3Cursor.close()
    sqlite3Conn.commit()
    sqlite3Conn.close()



"""
      增加对比结果
"""
def insertContrastResults(backupObjectName,differenceType,primaryKeyId,differenceField):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "INSERT INTO contrastResults(backupObjectName,differenceType,primaryKeyId,differenceField) VALUES('%s','%s','%s','%s');"%(backupObjectName,differenceType,primaryKeyId,differenceField)
    sqlite3Cursor.execute(sql)
    sqlite3Cursor.close()
    sqlite3Conn.commit()
    sqlite3Conn.close()
"""
      增加备份的表和应该备份的字段和对比主键
"""
def insertBackupFieldKey(objectName,fieldChosed,keyChosed,isSystemDefine,modifier,modificationTime):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "INSERT INTO backupFieldKey(objectName,fieldChosed,keyChosed,isSystemDefine,modifier,modificationTime) VALUES('%s','%s','%s','%s','%s','%s');"%(objectName,fieldChosed,keyChosed,isSystemDefine,modifier,modificationTime)
    sqlite3Cursor.execute(sql)
    sqlite3Cursor.close()
    sqlite3Conn.commit()
    sqlite3Conn.close()

insertBackupObject(1,'表1','backup4',1)
