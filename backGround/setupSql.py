#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: setupSql.py
@time: 2019/8/15 10:09
@function:
@inputParam:
@returnParam:
'''
import sqlite3




"""
      处理返回的一维列表
"""
def tuplesToList(fetchTuples):
    returnList = []
    if(len(fetchTuples[0])==1):
        for subTuple in fetchTuples:
            returnList.append(subTuple[0])
    else:
        print("输入不为1维")
    return returnList

"""
      获得模块列表
"""

def getMoudleInfo():
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "SELECT moudleName FROM moudleList"
    sqlite3Cursor.execute(sql)
    moudleInfo = sqlite3Cursor.fetchall()
    moudleInfo = tuplesToList(moudleInfo)
    sqlite3Conn.close()
    return moudleInfo

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
      删除一条新模块及配置的信息
"""
def deleteMoudleList(moudleName):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    moduleObjectsql = "delete from moudleObject where moduleName = %s and isSystemDefine = 0 "%(moudleName)
    modulesql = "delete from moudleList where moduleName = %s and isSystemDefine = 0 "%(moudleName)
    sqlite3Cursor.execute(moduleObjectsql)
    sqlite3Cursor.execute(modulesql)
    sqlite3Cursor.close()
    sqlite3Conn.commit()
    sqlite3Conn.close()

"""
        通过模块名查询对象
    需要输出的对象类型:type 1.表table 2.存储过程stored procedures 3.视图 view 
"""
def getObjectByModule(moduleName):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    tableSql = "SELECT objectName FROM moduleObject WHERE type = 1 AND modulename = %s"%(moduleName)
    storeSql = "SELECT objectName FROM moduleObject WHERE type = 2 AND modulename = %s"%(moduleName)
    viewSql = "SELECT objectName FROM moduleObject WHERE type = 3 AND modulename = %s"%(moduleName)
    sqlite3Cursor.execute(tableSql)
    tableName = sqlite3Cursor.fetchall()
    sqlite3Cursor.execute(storeSql)
    storeName = sqlite3Cursor.fetchall()
    sqlite3Cursor.execute(viewSql)
    viewName = sqlite3Cursor.fetchall()
    sqlite3Conn.close()
    return tableName,storeName,viewName



"""
       获得配置的表的主键和备份字段
"""
def getbackupFieldKey(tableName):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    fieldSql = 'SELECT fieldChosed from backupFieldKey where tableName = "%s" and fieldType = 1 '%(tableName)
    keySql = 'SELECT fieldChosed from backupFieldKey where tableName = "%s" and fieldType = 2'%(tableName)
    sqlite3Cursor.execute(fieldSql)
    fieldList = sqlite3Cursor.fetchall()
    sqlite3Cursor.execute(keySql)
    key = sqlite3Cursor.fetchall()
    sqlite3Conn.close()
    return fieldList,key



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
