#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: backupSql.py
@time: 2019/8/15 20:16
@function:
@inputParam:
@returnParam:
'''
import sqlite3
from backGround.testConnection import getOrcaleConnection,connectOracle,sqliteExecute,oracleExcute
from backGround.setupSql import getbackupFieldKey

"""
        检查是否存在sqlite库，没有则创建库
"""
def checkSystemDb():

    sql = "SELECT * FROM sqlite_master"

    system_table_info = sqliteExecute(sql)
    if (len(system_table_info) == 0):
        print("系统数据库信息不存在")
        count = 0  # 读取行数
        sql = ""  # 拼接的sql语句
        with open('DBBuild.sql', "r", encoding="utf-8") as f:
            for each_line in f.readlines():
                # 过滤数据
                if not each_line or each_line == "\n":
                    continue
                # 读取2000行数据，拼接成sql
                elif count < 2000:
                    sql += each_line
                    count += 1
                # 读取达到2000行数据，进行提交，同时，初始化sql，count值
                else:
                    sqliteExecute(sql)
                    sql = each_line
                    count = 1
                # 当读取完毕文件，不到2000行时，也需对拼接的sql 执行、提交
            if sql:
                sqliteExecute(sql)



def tuplesToList(fetchTuples):
    returnList = []
    if (len(fetchTuples) == 0):
        return
    if (len(fetchTuples[0]) == 1):
        for subTuple in fetchTuples:
            returnList.append(subTuple[0])
    else:
        for subTuple in fetchTuples:
            if (subTuple == None):
                returnList.append([])
            else:
                returnList.append(list(subTuple))
    return returnList


"""
      获得备份列表信息
"""
def getBackupInfomation():
    checkSystemDb()


    backInformationList = sqliteExecute("select backupVersion,backupTime from backupInformation")


    return backInformationList


"""
      创建新的备份
"""
def createBackupTable(timeList,tableList,processList,viewList):
    backupVersionId = getbackupVersionId()
    createBackupTable(timeList[0],timeList[1],tableList,backupVersionId)
    # createProcess(processList,backupVersionId)
    # createView(viewList,backupVersionId)




"""
      通过备份名获得备份详细内容
"""
def getBackupTime(backupVersion):
    checkSystemDb()

    backInformationList = sqliteExecute('select beginTime,endTime from backupInformation where backupVersion = "%s"'%(backupVersion))
    return backInformationList

"""
        通过备份版本查询对象
    需要输出的对象类型:type 1.表table 2.存储过程stored procedures 3.视图 view 
"""
def getObjectByVersion(backupVersion):

    sql = "SELECT objectName,objectType,backupObjectName FROM backupObjectNameList WHERE backupVersion =%s "%(backupVersion)
    objectList =     sqliteExecute(sql)
    return objectList
print(getObjectByVersion("1"))

"""
       获得新的备份的备份表目标id起始范围
"""
def getbackupObjectId():

    askSql = 'SELECT max(backupObjectName) from backupObjectNameList'
    version =     sqliteExecute(askSql)
    if (version == (None,)):
        backupObjectName = 1
    else:
        backupObjectName = int(version[0][6:]) + 1
    return backupObjectName

"""
       获得新的备份版本
"""
def getbackupVersionId():

    askSql = 'SELECT max(backupVersion) from backupInformation'
    versionList = sqliteExecute(askSql)

    if (versionList == (None,)):
        backupVersion = 1
    else:
        backupVersion = versionList[0] + 1

    return backupVersion

"""
        通过类型筛选查询对象
    需要输出的对象类型:type 1.表table 2.存储过程stored procedures 3.视图 view 
"""
def getObjectByType(typeCode):
    if(typeCode!=1&typeCode!=2&typeCode!=3):
        print("参数不合法")

    sql = "SELECT * FROM backupObjectNameList WHERE backupVersion ='' AND ObjectType = "+str(typeCode)+""
    objectList =  sqliteExecute(sql)
    return objectList


"""
      增加新的表备份
      输入参数：objectList 
      格式：[备份开始时间，备份截止时间，[对象名]，备份版本号] 

"""


def createBackupTable(beginTime, endTime, tableList, backupVersionId):
    startId = getbackupObjectId()

    for list in tableList:
        print(getbackupFieldKey(list[0]))
        fieldList = getbackupFieldKey(list[0])
        fieldList = fieldList[0]
        fieldStr = ''
        for field in fieldList:
            fieldStr += field[0] + ','
        lenthField = len(fieldStr)
        fieldStr = fieldStr[0:lenthField - 1]
        createSql = 'create table  %s as select %s from %s WHERE FDATE between %s and %s' \
                    % ('backup' + str(startId), fieldStr, list, beginTime, endTime)
        print(createSql)
        oracleExcute(createSql)
        insertNameListSql = 'insert into backupObjectNameList (backupVersion,objectName,backupObjectName,ObjectType) ' \
                            'values("%s","%s","%s",1)' % (backupVersionId, list, "backup" + str(startId))
        sqliteExecute(insertNameListSql)

        startId += 1

