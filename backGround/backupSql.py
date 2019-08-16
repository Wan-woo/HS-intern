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


"""
        检查是否存在sqlite库，没有则创建库
"""
def checkSystemDb():
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "SELECT * FROM sqlite_master"
    sqlite3Cursor.execute(sql)
    system_table_info = sqlite3Cursor.fetchall()
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
                    sqlite3Cursor.execute(sql)
                    sqlite3Conn.commit()
                    sql = each_line
                    count = 1
                # 当读取完毕文件，不到2000行时，也需对拼接的sql 执行、提交
            if sql:
                sqlite3Cursor.execute(sql)
                sqlite3Conn.commit()
                sqlite3Conn.close()

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
      获得备份列表
"""
def getBackupInfomation():
    checkSystemDb()
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sqlite3Cursor.execute("select backupVersion,backupTime from backupInformation")
    backInformationList = sqlite3Cursor.fetchall()
    backInformationList = tuplesToList(backInformationList)
    sqlite3Conn.close()
    return backInformationList
print(getBackupInfomation())
"""
      通过备份名获得备份详细内容
"""
def getBackupTime(backupVersion):
    checkSystemDb()
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sqlite3Cursor.execute('select beginTime,endTime from backupInformation where backupVersion = "%s"'%(backupVersion))
    backInformationList = sqlite3Cursor.fetchone()
    sqlite3Conn.close()
    return backInformationList

"""
        通过备份版本查询对象
    需要输出的对象类型:type 1.表table 2.存储过程stored procedures 3.视图 view 
"""
def getObjectByVersion(backupVersion):
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "SELECT objectName,objectType,backupObjectName FROM backupObjectNameList WHERE backupVersion =%s "%(backupVersion)
    sqlite3Cursor.execute(sql)
    objectList = sqlite3Cursor.fetchall()
    sqlite3Conn.close()
    return objectList
print(getObjectByVersion("1"))

"""
       获得新的备份的备份表id起始范围
"""
def getbackupObjectId():
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    askSql = 'SELECT max(backupObjectName) from backupObjectNameList'
    sqlite3Cursor.execute(askSql)
    version = sqlite3Cursor.fetchone()
    if (version == (None,)):
        backupObjectName = 1
    else:
        backupObjectName = int(version[0][6:]) + 1
    sqlite3Conn.close()
    return backupObjectName

"""
       获得新的备份版本
"""
def getbackupVersionId():
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    askSql = 'SELECT max(backupVersion) from backupInformation'
    sqlite3Cursor.execute(askSql)
    versionList = sqlite3Cursor.fetchone()
    if (versionList == (None,)):
        backupVersion = 1
    else:
        backupVersion = versionList[0] + 1
    sqlite3Conn.close()
    return backupVersion

"""
        通过类型筛选查询对象
    需要输出的对象类型:type 1.表table 2.存储过程stored procedures 3.视图 view 
"""
def getObjectByType(typeCode):
    if(typeCode!=1&typeCode!=2&typeCode!=3):
        print("参数不合法")
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    sql = "SELECT * FROM backupObjectNameList WHERE backupVersion ='' AND ObjectType = "+str(typeCode)+""
    sqlite3Cursor.execute(sql)
    objectList = sqlite3Cursor.fetchall()
    sqlite3Conn.close()
    return objectList

