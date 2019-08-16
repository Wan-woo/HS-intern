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
from backGround.testConnection import getOrcaleConnection,getSqliteConnection



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
        获取功能指标列表
"""
def getFunctionQuotaInfo():
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    functionSql = "SELECT functionQuotaName FROM functionQuotaList where functionQuotaType=1"
    quotaSql = "SELECT functionQuotaName FROM functionQuotaList where functionQuotaType=2"
    sqlite3Cursor.execute(functionSql)
    functionList = sqlite3Cursor.fetchall()
    functionList = tuplesToList(functionList)
    sqlite3Cursor.execute(quotaSql)
    quotaList = sqlite3Cursor.fetchall()
    quotaList = tuplesToList(quotaList)
    sqlite3Conn.close()
    return functionList,quotaList

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
      增加一个新模块
"""
def insertModuleList(moduleName):
    sqlite3Conn = getSqliteConnection()
    sql = "INSERT INTO ModuleList(moduleName,isSystemDefineModule) VALUES('%d',0);"%(moduleName)
    sqlite3Conn.execute(sql)
    sqlite3Conn.commit()
    sqlite3Conn.close()
"""
      获得当前Oracle中所有表存储过程视图
"""

def getOracleInfo():
    oracleConn = getOrcaleConnection()
    oracleCursor = oracleConn.cursor()
    oracleCursor.execute("Select object_name From user_objects Where object_type='TABLE' ")
    tableList = oracleCursor.fetchall()
    tableList =  tuplesToList(tableList)
    oracleCursor.execute("Select object_name From user_objects Where object_type='PROCEDURE' ")
    produceList = oracleCursor.fetchall()
    produceList =  tuplesToList(produceList)
    oracleCursor.execute("Select object_name From user_objects Where object_type='VIEW' ")
    viewList = oracleCursor.fetchall()
    viewList =  tuplesToList(viewList)
    return [tableList,produceList,viewList]
print(getOracleInfo())

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
      删除一个模块及关于此模块的配置的信息
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
      删除一条配置信息
"""
def deleteMoudleList(setupList):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    for setup in setupList:
        if (setup[2] == '表'):
            setup[2] = 1
        elif (setup[2] == "存储过程"):
            setup[2] = 2
        elif (setup[2] == "视图"):
            setup[2] = 3
        moduleObjectsql = "delete from moudleObject where moduleName = '%s' and objectName='%s'" \
                          " and objectName='%d' and isSystemDefine = 0 "%(setup[0],setup[1],setup[2])

    sqlite3Cursor.execute(moduleObjectsql)
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



# """
#       接收新增的字典用于新增配置记录（给前端调用）
# """
def insertMoudleObjectsField(dicts1,dicts2):
    moudleName = dicts1.get('module')
    functionList = dicts1.get('function')
    quotaList = dicts1.get('quota')
    tableList = dicts1.get('table')
    processList = dicts1.get('process')
    viewList = dicts1.get('view')
    sqliteConn = getSqliteConnection()
    """"
        新增配置关系
    """
    if len(tableList)!=0:
        for objectName in tableList:
            tableSql = "insert into moduleObject (moudleName,objectName,objectType,isSystemDefine) values ('%s','%s',1,0)"%(moudleName,objectName)
            sqliteConn.execute(tableSql)
    if len(processList)!=0:
        for objectName in processList:
            processSql = "insert into moduleObject (moudleName,objectName,objectType,isSystemDefine) values ('%s','%s',1,0)"%(moudleName,objectName)
            sqliteConn.execute(processSql)
    if len(viewList)!=0:
        for objectName in viewList:
            viewSql = "insert into moduleObject (moudleName,objectName,objectType,isSystemDefine) values ('%s','%s',1,0)"%(moudleName,objectName)
            sqliteConn.execute(viewSql)
    """
        新增备份字段与对比主键 
    """
    for table in tableList:
        backupFileds =dicts2.get(table).get('field')
        keyFields = dicts2.get(table).get('key')
        for backupFiled in backupFileds:
            fieldSql = "insert into backupFieldKey (tableName,fieldChosed,fieldType,isSystemDefine) values " \
                       "('%s','%s',1,0)"%(table,backupFiled)
            sqliteConn.execute(fieldSql)
        for backupFiled in keyFields:
            keySql = "insert into backupFieldKey (tableName,fieldChosed,fieldType,isSystemDefine) values " \
                       "('%s','%s',2,0)"%(table,backupFiled)
            sqliteConn.execute(keySql)




returnDict = {'module': '模块一', 'function': ['C', 'C++'], 'quota': ['Java', 'JavaScript'], 'process': ['C'], 'view': ['JavaScript'], 'table': ['JavaScript']}
returnTableDict = {'JavaScript': {'key': ['id'], 'field': ['id']}}



