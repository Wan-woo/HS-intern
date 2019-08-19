#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: contrast.py
@time: 2019/8/14 15:41
@function:
@inputParam:
@returnParam:
'''
from backGround.backupSql import getBackupTime,getObjectByVersion
from backGround.setupSql import tuplesToList
from backGround.testConnection import getSqliteConnection,getOrcaleConnection
def makeContrasr(backupVersion):
    [beginTime,endTime]=getBackupTime(backupVersion)
    objectList = getObjectByVersion(backupVersion)
    tableList = []
    backupTableList = []
    sqliteConn = getSqliteConnection()
    sqliteCursor = sqliteConn.cursor()
    for object in objectList:
        if object[1]:
            tableList.append(object[0])
            backupTableList.append(object[2])
    for index in range(len(tableList)):
        keySql = "select fieldChosed from backupFieldKey where tableName = %s and fieldType = 2 "%(tableList[index])
        fieldSql = "select fieldChosed from backupFieldKey where tableName = %s and fieldType = 2 "%(tableList[index])
        sqliteCursor.execute(keySql)
        keyList = sqliteCursor.fetchall()
        keyList = tuplesToList(keyList)
        keyStr = fieldListToStr(keyList)
        sqliteCursor.execute(fieldSql)
        fieldList = tuplesToList(sqliteCursor.fetchall())
        fieldStr = fieldListToStr(fieldList)

        deleteSql = 'select "%s" from "%s" MINUS select "%s" from "%s" where FDATE BETWEEN "%s"  AND "%s"'%(keyList,tableList[index],keyList,backupTableList[index],beginTime,endTime)
        insertSql = 'select "%s" from "%s" MINUS select "%s" from "%s" where FDATE BETWEEN "%s"  AND "%s"'%(keyList,backupTableList[index],keyList,tableList[index],beginTime,endTime)
        sameSql = 'select "%s" from "%s" intersect select "%s" from "%s" where FDATE BETWEEN "%s"  AND "%s"'%(fieldList,tableList[index],fieldList,backupTableList[index],beginTime,endTime)
        updateSql = '(select "%s" from "%s" intersect select "%s" from "%s" where FDATE BETWEEN "%s"  AND "%s")minus (%s)'%(fieldList,tableList[index],fieldList,backupTableList[index],beginTime,endTime,sameSql)




def fieldListToStr(fieldList):
    fieldStr=""
    for field in fieldList:
        fieldList+=field
    return fieldStr
