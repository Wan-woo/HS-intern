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
from backGround.testConnection import getOrcaleConnection,getSqliteConnection,oracleExcute,sqliteExecute,oracleNoFetch


"""
      处理返回的一维列表
"""
def tuplesToList(fetchTuples):
    returnList = []
    if(len(fetchTuples)==0):
        return []
    if(len(fetchTuples[0])==1):
        for subTuple in fetchTuples:

            returnList.append(subTuple[0])
    else:
        for subTuple in fetchTuples:
            if(subTuple==None):
                returnList.append([])
            else:
                returnList.append(list(subTuple))
    return returnList


"""
        获取功能指标列表
"""
def getFunctionQuotaInfo():

    functionSql = "SELECT functionQuotaName FROM functionQuotaList where functionQuotaType=1"
    quotaSql = "SELECT functionQuotaName FROM functionQuotaList where functionQuotaType=2"

    functionList = sqliteExecute(functionSql)


    quotaList = sqliteExecute(quotaSql)


    return functionList,quotaList

"""
      获得模块列表
"""

def getModuleInfo():
    sql = "SELECT moduleName FROM moduleList"
    moduleInfo = sqliteExecute(sql)


    return moduleInfo
print(getModuleInfo())

"""
      增加一个新模块
"""
def insertModule(moduleName):

    sql = "INSERT INTO moduleList(moduleName,isSystemDefine) VALUES('%s',0);"%(moduleName)
    sqliteExecute(sql)
"""
      获得当前Oracle中所有表存储过程视图
"""

def getOracleInfo():

    tableList = oracleExcute("Select object_name From user_objects Where object_type='TABLE' ")
    try:
        tableList.index("CONTRASTRESULTS")
    except ValueError :
        sql = 'CREATE TABLE "CONTRASTRESULTS"  ' \
              ' (	"ID" NUMBER(*,0) NOT NULL ENABLE,	"BACKUPOBJECTNAME" VARCHAR2(4000),' \
              '"RECORDID" NUMBER(*,0),	"PRIMARYKEYNAME" VARCHAR2(4000),	' \
              '"PRIMARYKEYVALUE" VARCHAR2(4000),	"DIFFERENCETYPE" NUMBER(*,0)   ) '
        oracleNoFetch(sql)
    produceList = oracleExcute("Select object_name From user_objects Where object_type='PROCEDURE' ")

    viewList = oracleExcute("Select object_name From user_objects Where object_type='VIEW' ")

    fieldDicts={}
    for table in tableList:
        fieldSql = "select COLUMN_NAME from USER_COL_COMMENTS where table_name = '%s'"%(table)

        fieldList = oracleExcute(fieldSql)

        fieldDicts[table]=fieldList
    return [tableList,produceList,viewList,fieldDicts]
print(getOracleInfo())

"""
      获得所有配置信息
"""
def getSetupList():

    moduleObjectSql = "select moduleName,objectName,objectType from moduleObject"
    print(moduleObjectSql)

    moduleObjects =sqliteExecute(moduleObjectSql)

    if(len(moduleObjects)==0):
        return
    for moduleObject in moduleObjects:
        functionSql  = "select functionQuotaName from objectFunctionQuota where objectName = '%s' and objectType='%s' and functionQuotaType=1"%(moduleObject[1],moduleObject[2])
        result=sqliteExecute(functionSql)


        moduleObject.append(result)
        quotaSql  = "select functionQuotaName from objectFunctionQuota where objectName = '%s' and objectType='%s' and functionQuotaType=2"%(moduleObject[1],moduleObject[2])
        result= sqliteExecute(quotaSql)

        moduleObject.append(result)
        if(moduleObject[2]==1):
            moduleObject[2]="表"
        elif(moduleObject[2]==2):
            moduleObject[2] = "存储过程"
        elif(moduleObject[2]==3):
            moduleObject[2]="视图"
    return moduleObjects
print(getSetupList())

"""
      删除一个模块及关于此模块的配置的信息
"""
def deleteModule(moduleName):

    moduleObjectsql = "delete from moduleObject where moduleName = '%s' and isSystemDefine = 0 "%(moduleName)
    modulesql = "delete from moduleList where moduleName = '%s' and isSystemDefine = 0 "%(moduleName)
    sqliteExecute(moduleObjectsql)
    sqliteExecute(modulesql)


"""
      删除一条配置信息
"""
def deleteModuleList(setupList):



    if (setupList[2] == "表"):
        setupList[2] = 1
    elif (setupList[2] == "存储过程"):
        setupList[2] = 2
    elif (setupList[2] == "视图"):
        setupList[2] = 3
    moduleObjectsql = "delete from moduleObject where moduleName = '%s' and objectName='%s' and objectType='%s' and isSystemDefine= '0' "%(setupList[0],setupList[1],setupList[2])

    sqliteExecute(moduleObjectsql)

"""
        通过模块名查询对象
    需要输出的对象类型:type 1.表table 2.存储过程stored procedures 3.视图 view 
"""
def getObjectByModule(moduleName):

    tableSql = "SELECT objectName FROM moduleObject WHERE type = 1 AND modulename = %s"%(moduleName)
    processSql = "SELECT objectName FROM moduleObject WHERE type = 2 AND modulename = %s"%(moduleName)
    viewSql = "SELECT objectName FROM moduleObject WHERE type = 3 AND modulename = %s"%(moduleName)

    tableName = sqliteExecute(tableSql)


    processName = sqliteExecute(processSql)


    viewName = sqliteExecute(viewSql)


    return tableName,processName,viewName



"""
       获得配置的表的主键和备份字段
"""
def getbackupFieldKey(tableName):

    fieldSql = 'SELECT fieldChosed from backupFieldKey where tableName = "%s" and fieldType = 1 '%(tableName)
    keySql = 'SELECT fieldChosed from backupFieldKey where tableName = "%s" and fieldType = 2'%(tableName)
    fieldList = sqliteExecute(fieldSql)

    key = sqliteExecute(keySql)

    return fieldList,key



# """
#       接收新增的字典用于新增配置记录（给前端调用）
# """
def insertModuleObjectsField(dicts1,dicts2):
    moduleName = dicts1.get('module')
    functionList = dicts1.get('function')
    quotaList = dicts1.get('quota')
    tableList = dicts1.get('table')
    processList = dicts1.get('process')
    viewList = dicts1.get('view')

    """"
        新增配置关系
    """
    if len(tableList)!=0:
        for objectName in tableList:
            tableSql = "insert into moduleObject (moduleName,objectName,objectType,isSystemDefine) values ('%s','%s',1,0)"%(moduleName,objectName)
            sqliteExecute(tableSql)
    if len(processList)!=0:
        for objectName in processList:
            processSql = "insert into moduleObject (moduleName,objectName,objectType,isSystemDefine) values ('%s','%s',1,0)"%(moduleName,objectName)
            sqliteExecute(processSql)
    if len(viewList)!=0:
        for objectName in viewList:
            viewSql = "insert into moduleObject (moduleName,objectName,objectType,isSystemDefine) values ('%s','%s',1,0)"%(moduleName,objectName)
            sqliteExecute(viewSql)

    """
        新增备份字段与对比主键 
    """
    for table in tableList:
        for table in tableList:
            backupFileds = dicts2.get(table).get('field')
            keyFields = dicts2.get(table).get('key')
            for backupFiled in backupFileds:
                fieldSql = "insert into backupFieldKey (tableName,fieldChosed,fieldType,isSystemDefine) values " \
                           "('%s','%s',1,0)" % (table, backupFiled)
                sqliteExecute(fieldSql)
            for backupFiled in keyFields:
                keySql = "insert into backupFieldKey (tableName,fieldChosed,fieldType,isSystemDefine) values " \
                         "('%s','%s',2,0)" % (table, backupFiled)
                sqliteExecute(keySql)

    """
           新增functionQuota与object对应
    """
    # for table in tableList:
    #     for function in functionList:
    #         fieldSql = "insert into objectFunctionQuota (objectName,objectType,functionQuotaName,functionQuotaType) values " \
    #                    "('%s',1,'%s',1,0)" % (table, backupFiled)
    #         sqliteConn.execute(fieldSql)
    #     for quota in quotaList:
    #         keySql = "insert into objectFunctionQuota (tableName,fieldChosed,fieldType,isSystemDefine) values " \
    #                  "('%s','%s',2,0)" % (table, backupFiled)
    #         sqliteConn.execute(keySql)

"""
    修改当前存在对比的版本
"""
def changeCurContrast(backupVersion):
    removeSql = "update backupInformation set hasContrast = 0 "
    setSql = "update backupInformation set hasContrast = 1 where backupVersion='%s'"(backupVersion)
    sqliteExecute(removeSql)
    sqliteExecute(setSql)
# returnDict = {'module': '模块1', 'function': [], 'quota': [], 'process': [], 'view': [], 'table': ['COURSE']}
# returnTableDict = {'COURSE': {'key': ['CNAME'], 'field': ['CNO', 'TNO', 'CNAME']}}
# print(insertModuleObjectsField(returnDict,returnTableDict))


