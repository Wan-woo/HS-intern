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
from backGround.testConnection import getSqliteConnection,getOrcaleConnection,sqliteExecute,oracleExcute
def fieldListToStr(fieldList):
    fieldStr=""
    for index in range(len(fieldList)):
        fieldStr+=fieldList[index]
        if len(fieldList)-1>index:
            fieldStr+=','
    return fieldStr
def makeContrasr(backupVersion):
    [[beginTime,endTime],]=getBackupTime(backupVersion)
    objectList = getObjectByVersion(backupVersion)
    tableList = []
    backupTableList = []

    for object in objectList:
        if object[1]==1:
            tableList.append(object[0])
            backupTableList.append(object[2])
    for index in range(len(tableList)):
        keySql = "select fieldChosed from backupFieldKey where tableName = '%s' and fieldType = 2 "%(tableList[index])
        fieldSql = "select fieldChosed from backupFieldKey where tableName = '%s' "%(tableList[index])

        keyList = sqliteExecute(keySql)
        keyStr = fieldListToStr(keyList)

        fieldList = sqliteExecute(fieldSql)

        fieldStr = fieldListToStr(fieldList)

        deleteSql = 'select %s from %s MINUS select %s from %s where FDATE BETWEEN %s  AND %s'%(keyStr,tableList[index],keyStr,backupTableList[index],beginTime,endTime)
        insertSql = 'select %s from %s MINUS select %s from %s where FDATE BETWEEN %s  AND %s'%(keyStr,backupTableList[index],keyStr,tableList[index],beginTime,endTime)
        sameSql = 'select %s from (select %s from %s intersect select %s from %s where FDATE BETWEEN %s  AND %s)'%(keyStr,fieldStr,tableList[index],fieldStr,backupTableList[index],beginTime,endTime)
        updateSql = '(select %s from %s intersect select %s from %s where FDATE BETWEEN %s  AND %s)minus ' \
                    '(select %s from (%s))'%(keyStr,tableList[index],keyStr,backupTableList[index],beginTime,endTime,keyStr,sameSql)


        deleteList = oracleExcute(deleteSql)
        insertList = oracleExcute(insertSql)
        sameList = oracleExcute(sameSql)
        updateList = oracleExcute(updateSql)

        getRecordSql = "select MAX(recordId) from CONTRASTRESULTS"
        id = oracleExcute(getRecordSql)[0]
        if id==None:
            id=0
        else:
            id+=1
        print(id)
        for deleteRecord in deleteList:
            insertResultSql = "insert into contrastResults(backupObjectName,recordId,primaryKeyName,primaryKeyId,differenceType)" \
                          "values ('%s','%s','%s','%s','%s')"%(tableList[index],recordId,primaryKeyName,primaryKeyId,"1")

        print(updateSql)
    return deleteList,insertList,sameList,updateList
contrasrList = makeContrasr(5)
print(contrasrList[0])
print(contrasrList[1])
print(contrasrList[2])
print(contrasrList[3])


