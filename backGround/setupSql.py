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
    if(len(fetchTuples)==0):
        return
    if(len(fetchTuples[0])==1):
        for subTuple in fetchTuples:
            returnList.append(subTuple[0])
    else:
        for subTuple in fetchTuples:
            returnList.append(list(subTuple))
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
print(getMoudleInfo())

"""
      获得所有配置信息
"""
def getSetupList():
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    moduleObjectSql = "select moduleName,objectName,objectType from moduleObject"
    print(moduleObjectSql)
    sqlite3Cursor.execute(moduleObjectSql)
    moudleObjects =sqlite3Cursor.fetchall()
    moudleObjects = tuplesToList(moudleObjects)
    if(len(moudleObjects)==0):
        return
    for moduleObject in moudleObjects:
        functionSql  = "select functionQuotaName from objectFunctionQuota where objectName = '%s' and objectType='%s' and functionQuotaType=1"%(moduleObject[1],moduleObject[2])
        sqlite3Cursor.execute(functionSql)
        result=sqlite3Cursor.fetchall()
        result=tuplesToList(result)
        moduleObject.append(result)
        quotaSql  = "select functionQuotaName from objectFunctionQuota where objectName = '%s' and objectType='%s' and functionQuotaType=2"%(moduleObject[1],moduleObject[2])
        sqlite3Cursor.execute(quotaSql)
        result=sqlite3Cursor.fetchall()
        result=tuplesToList(result)
        moduleObject.append(result)
        if(moduleObject[2]==1):
            moduleObject[2]="表"
        elif(moduleObject[2]==2):
            moduleObject[2] = "存储过程"
        elif(moduleObject[2]==3):
            moduleObject[2]="视图"

    sqlite3Cursor.close()
    sqlite3Conn.close()
    return moudleObjects
print(getSetupList())

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
      接收新增的字典用于新增记录（给前端调用）
"""
# def insertMoudleObjects(dicts1,dicts2):
#     for dict in dicts1:
#         moduleName = dict.


"""
      增加一条模块与对象对应关系（底层不用来调用）
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
