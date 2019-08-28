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
from backGround.testConnection import getOrcaleConnection,connectOracle,sqliteExecute,oracleExcute,oracleNoFetch,getSqliteConnection
from backGround.setupSql import getbackupFieldKey,listsToList
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
fp = logging.FileHandler('log.txt', encoding='utf-8')
fs = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])    # 调用

"""
        检查是否存在sqlite库，没有则创建库
"""
def checkSystemDb():

    sql = "SELECT * FROM sqlite_master"

    system_table_info = sqliteExecute(sql)
    if (len(system_table_info) == 0):
        logging.info("系统数据库信息不存在")
        count = 0  # 读取行数
        sql = ""  # 拼接的sql语句
        with open('DBBuild.sql', "r", encoding="utf-8") as f:
            for each_line in f.readlines():
                # 过滤数据
                if not each_line or each_line == "\n":
                    continue
                # 读取2000行数据，拼接成sql
                else:
                    sql += each_line
                    count += 1
                # 读取达到2000行数据，进行提交，同时，初始化sql，count值

                # 当读取完毕文件，不到2000行时，也需对拼接的sql 执行、提交
        sqlList = sql.split(";")
        sqliteConn =  getSqliteConnection()
        sqliteCusor = sqliteConn.cursor()
        try:
            for subSqlList in sqlList:
                sqliteCusor.execute(subSqlList)
        except sqlite3.Error as msg:
            logging.debug(msg)
            logging.debug(subSqlList)
        sqliteConn.commit()
        sqliteConn.close()

# logging.info(checkSystemDb())

def tuplesToList(fetchTuples):
    returnList = []
    if (len(fetchTuples) == 0):
        return


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
def createNewBackup(timeList,tableList,processList,viewList):
    backupVersionId = getbackupVersionId()
    createBackupTable(timeList[0],timeList[1],tableList,backupVersionId)
    # createProcess(processList,backupVersionId)
    # createView(viewList,backupVersionId)
    insertBackupInformation(backupVersionId,timeList[0],timeList[1])

"""
    删除某个备份
"""
def deleteBackup(backupVersion):
    tableList = getObjectByVersion(backupVersion)[0]
    for table in tableList:
        delTableSql = "drop table %s "%('backup'+str(table[1]))
        oracleNoFetch(delTableSql)
    delBackupObjectNameList = "delete from backupObjectNameList where backupVersion = '%s' "%(backupVersion)
    delBackupInformation = "delete from backupInformation where backupVersion = '%s' "%(backupVersion)
    sqliteExecute(delBackupInformation)
    sqliteExecute(delBackupObjectNameList)
"""
      通过备份名获得备份时间
"""
def getBackupTime(backupVersion):
    checkSystemDb()

    backInformationList = sqliteExecute('select beginTime,endTime from backupInformation where backupVersion = "%s"'%(backupVersion))
    return backInformationList

"""
        通过备份版本查询对象
    需要输出的对象类型:二维列表组
"""
def getObjectByVersion(backupVersion):

    tableSql = "SELECT objectName,backupObjectName FROM backupObjectNameList WHERE backupVersion =%s and objectType='1'"%(backupVersion)
    processSql = "SELECT objectName,backupObjectName FROM backupObjectNameList WHERE backupVersion =%s and objectType='2'"%(backupVersion)
    viewSql = "SELECT objectName,backupObjectName FROM backupObjectNameList WHERE backupVersion =%s and objectType='3'"%(backupVersion)
    tableList = sqliteExecute(tableSql)

    processList = sqliteExecute(processSql)

    viewList = sqliteExecute(viewSql)

    return tableList,processList,viewList


"""
       获得新的备份的备份表目标id起始范围
"""
def getbackupObjectId():

    askSql = 'SELECT max(backupObjectName) from backupObjectNameList'
    version =  sqliteExecute(askSql)[0]

    logging.info(len(version))
    if ((len(version)==0)|(version[0]=='')|(version[0]==None)):
        backupObjectName = 1
    else:
        backupObjectName = int(version[0]) + 1
    return backupObjectName

"""
       获得新的备份版本
"""
def getbackupVersionId():

    askSql = 'SELECT max(backupVersion) from backupInformation'
    versionList = sqliteExecute(askSql)
    versionList = listsToList(versionList)
    if (versionList == [None]):
        backupVersion = 1
    else:
        backupVersion = versionList[0] + 1

    return backupVersion

"""
    在backupInformation中插入备份信息
"""
def insertBackupInformation(backupVersion,beginTime,endTime):
    getDataSql = "select datetime(CURRENT_TIMESTAMP,'localtime');"
    curData = sqliteExecute(getDataSql)[0][0]
    insertSql = "insert into backupInformation (backupVersion,backupTime,beginTime,endTime,hasContrast)values('%s','%s','%s','%s','%s') "%(backupVersion,curData,beginTime,endTime,0)
    sqliteExecute(insertSql)
"""
        通过类型筛选查询对象
    需要输出的对象类型:type 1.表table 2.存储过程stored procedures 3.视图 view 
"""
def getObjectByType(typeCode):
    if(typeCode!=1&typeCode!=2&typeCode!=3):
        logging.info("参数不合法")

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
        logging.info(getbackupFieldKey(list))
        fieldList = getbackupFieldKey(list)
        fieldList = fieldList[0]
        fieldStr = ''
        for field in fieldList:
            fieldStr += field + ','
        lenthField = len(fieldStr)
        fieldStr = fieldStr[0:lenthField - 1]
        if 'CREATE_DATE' in fieldList:
            createSql = 'create table  %s as select %s from %s WHERE CREATE_DATE between %s and %s' \
                        % ('backup' + str(startId), fieldStr, list, beginTime, endTime)
        elif 'VC_UPDATETIME' in fieldList:
            createSql = 'create table  %s as select %s from %s WHERE VC_UPDATETIME between %s and %s' \
                        % ('backup' + str(startId), fieldStr, list, str(beginTime)+'000000',str(endTime)+'000000')
        else:
            createSql = 'create table  %s as select %s from %s ' \
                        % ('backup' + str(startId), fieldStr, list)
        #无时间
        #createSql = 'create table  %s as select %s from %s ' \
        #             % ('backup' + str(startId), fieldStr, list)
        logging.info(createSql)
        oracleNoFetch(createSql)
        insertNameListSql = 'insert into backupObjectNameList (backupVersion,objectName,backupObjectName,ObjectType) ' \
                            'values("%s","%s","%s",1)' % (backupVersionId, list, startId)
        sqliteExecute(insertNameListSql)

        startId += 1

