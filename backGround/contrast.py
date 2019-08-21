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
from backGround.backupSql import getBackupTime,getObjectByVersion,listsToList
from backGround.setupSql import changeCurContrast,getbackupFieldKey
from backGround.testConnection import getSqliteConnection,getOrcaleConnection,sqliteExecute,oracleExcute,oracleNoFetch
import cx_Oracle


"""
        根据表名与类型查询对比结果，类型：1.删除 (del) 2.新增(insert) 3.相同(same) 4.更改(update) 5.不同（different）6.全部(all)
            分页
"""
def getResultByTableNameAndType(tableName,type):
    baseSql  = "select * from contrastResults where BACKUPOBJECTNAME = %s "%(tableName)
    if str(type)==1:
        endSql = baseSql+"and DIFFERENCETYPE = '1'"
    elif str(type)==2:
        endSql = baseSql+"and DIFFERENCETYPE = '2'"
    elif str(type)==3:
        endSql = baseSql+"and DIFFERENCETYPE = '3'"
    elif str(type)==4:
        endSql = baseSql+"and DIFFERENCETYPE = '4'"
    elif str(type)==5:
        endSql = baseSql+"and DIFFERENCETYPE = '2' or DIFFERENCETYPE = '1' or DIFFERENCETYPE = '4' "
    elif str(type)==2:
        endSql = baseSql
"""
    根据表名获取不同差异类型的个数
    输入格式 表名  示例  'S_FA_YSS_GZB'
    返回格式 一维数字列表 示例 [0, 0, 16444, 0]
    
"""
def getDiffNumByTableName(tableName):

    keyList = getbackupFieldKey(tableName)[1]
    keyNum = len(keyList)
    if(keyNum==0):
        return [0,0,0,0]
    else:
        returnNums = []
        for i in range(4):
            searchSql = "select count(*) from contrastResults where BACKUPOBJECTNAME = '%s' and DIFFERENCETYPE = %s"%(tableName,str(i+1))
            returnNums.append(oracleExcute(searchSql)[0][0]//keyNum)
    return returnNums


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
    truncateSql = "truncate table contrastResults"
    oracleNoFetch(truncateSql)

    [[beginTime,endTime],]=getBackupTime(backupVersion)

    tableAndBackupList = getObjectByVersion(backupVersion)[0]

    tableList = []
    backupTableList = []

    for object in tableAndBackupList:
        tableList.append(object[0])
        backupTableList.append('backup'+str(object[1]))
    for index in range(len(tableList)):

        [fieldList,keyList] = getbackupFieldKey(tableList[index])


        fieldStr = fieldListToStr(fieldList)
        keyStr = fieldListToStr(keyList)

        # deleteSql = 'select %s from %s MINUS select %s from %s where FDATE BETWEEN %s  AND %s'%(keyStr,tableList[index],keyStr,backupTableList[index],beginTime,endTime)
        # insertSql = 'select %s from %s MINUS select %s from %s where FDATE BETWEEN %s  AND %s'%(keyStr,backupTableList[index],keyStr,tableList[index],beginTime,endTime)
        # sameSql = 'select %s from (select %s from %s intersect select %s from %s where FDATE BETWEEN %s  AND %s)'%(keyStr,fieldStr,tableList[index],fieldStr,backupTableList[index],beginTime,endTime)
        # updateSql = '(select %s from %s intersect select %s from %s where FDATE BETWEEN %s  AND %s)minus ' \
        #             '(select %s from (%s))'%(keyStr,tableList[index],keyStr,backupTableList[index],beginTime,endTime,keyStr,sameSql)
        deleteSql = 'select %s from %s MINUS select %s from %s '%(keyStr,tableList[index],keyStr,backupTableList[index])
        insertSql = 'select %s from %s MINUS select %s from %s '%(keyStr,backupTableList[index],keyStr,tableList[index])
        sameSql = 'select %s from (select %s from %s intersect select %s from %s )'%(keyStr,fieldStr,tableList[index],fieldStr,backupTableList[index])
        updateSql = '(select %s from %s intersect select %s from %s )minus ' \
                    '(select %s from (%s))'%(keyStr,tableList[index],keyStr,backupTableList[index],keyStr,sameSql)

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
    recordId = oracleExcute(getRecordSql)[0][0]
    if recordId==None:
        recordId=0
    else:
        recordId=recordId+1

    getIdSql = "select MAX(ID) from CONTRASTRESULTS"
    id = oracleExcute(getIdSql)[0][0]
    if id==None:
        id=0
    else:
        id+=1
    oracleConn = getOrcaleConnection()
    oracleCursor = oracleConn.cursor()
    try:
        if deleteList!=None:
            recordType = "1"
            for record in deleteList:
                for keyIndex in range(len(keyList)):
                    insertResultSql = "insert into contrastResults values('%s','%s','%s','%s','%s','%s')"%(id,tableName,recordId,keyList[keyIndex],record[keyIndex],recordType)
                    oracleCursor.execute(insertResultSql)
                    id+=1
                recordId+=1
        if insertList != None:
            recordType = "2"
            for record in insertList:
                for keyIndex in range(len(keyList)):
                    insertResultSql = "insert into contrastResults values('%s','%s','%s','%s','%s','%s')"%(id,tableName,recordId,keyList[keyIndex],record[keyIndex],recordType)
                    oracleCursor.execute(insertResultSql)
                    id+=1
                recordId+=1
        if sameList != None:
            recordType = "3"
            for record in sameList:

                for keyIndex in range(len(keyList)):
                    insertResultSql = "insert into contrastResults values('%s','%s','%s','%s','%s','%s')"%(id,tableName,recordId,keyList[keyIndex],record[keyIndex],recordType)
                    oracleCursor.execute(insertResultSql)
                    id+=1
                recordId+=1
        if updateList != None:
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


# contrasrList = makeContrasr(5)



