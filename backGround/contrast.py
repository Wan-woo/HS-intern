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
from backGround.setupSql import changeCurContrast
from backGround.testConnection import getSqliteConnection,getOrcaleConnection,sqliteExecute,oracleExcute,oracleNoFetch
import cx_Oracle


"""
        修改问题
"""

"""
        将列表类型的字段转换成sql中字段的字符串格式
        输入：[字段1，字段2]
        输出："字段1，字段2"
"""
def fieldListToStr(fieldList):
    fieldStr=""
    for index in range(len(fieldList)):
        fieldStr+=fieldList[index]
        if len(fieldList)-1>index:
            fieldStr+=','
    return fieldStr

"""
        根据备份版本进行对比，并将对比结果保存起来（通过调用saveContrast）
        输入：备份版本
        输入示例："3"
        输出：无
"""
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

        saveContrast(tableList[index],keyList,deleteList,insertList,sameList,updateList)
    changeCurContrast(backupVersion)
"""
        接收对比结果并将对比结果存储到contrastResults
        输入：tableName,keyList,deleteList,insertList,sameList,updateList
        输入示例：
        输出：无
"""
def saveContrast(tableName,keyList,deleteList,insertList,sameList,updateList):
    getRecordSql = "select MAX(recordId) from CONTRASTRESULTS"
    recordId = oracleExcute(getRecordSql)[0]
    if recordId==None:
        recordId=0
    else:
        recordId+=1

    getIdSql = "select MAX(ID) from CONTRASTRESULTS"
    id = oracleExcute(getIdSql)[0]
    if id==None:
        id=0
    else:
        id+=1
    oracleConn = getOrcaleConnection()
    oracleCursor = oracleConn.cursor()
    try:
        recordType = "1"
        for record in deleteList:
            for keyIndex in range(len(keyList)):
                insertResultSql = "insert into contrastResults values('%s','%s','%s','%s','%s','%s')"%(id,tableName,recordId,keyList[keyIndex],record[keyIndex],recordType)
                oracleCursor.execute(insertResultSql)
                id+=1
            recordId+=1

        recordType = "2"
        for record in insertList:
            for keyIndex in range(len(keyList)):
                insertResultSql = "insert into contrastResults values('%s','%s','%s','%s','%s','%s')"%(id,tableName,recordId,keyList[keyIndex],record[keyIndex],recordType)
                oracleCursor.execute(insertResultSql)
                id+=1
            recordId+=1

        recordType = "3"
        for record in sameList:

            for keyIndex in range(len(keyList)):
                insertResultSql = "insert into contrastResults values('%s','%s','%s','%s','%s','%s')"%(id,tableName,recordId,keyList[keyIndex],record[keyIndex],recordType)
                oracleCursor.execute(insertResultSql)
                id+=1
            recordId+=1

        recordType = "4"
        for record in updateList:

            for keyIndex in range(len(keyList)):
                insertResultSql = "insert into contrastResults values('%s','%s','%s','%s','%s','%s')"%(id,tableName,recordId,keyList[keyIndex],record[keyIndex],recordType)
                oracleCursor.execute(insertResultSql)
                id+=1
            recordId+=1
        # print(updateSql)
    except cx_Oracle.DatabaseError as Err:
        print(Err)
    oracleConn.commit()
    oracleConn.close()
    return deleteList,insertList,sameList,updateList


contrasrList = makeContrasr(5)



