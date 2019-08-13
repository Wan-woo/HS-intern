#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: createBackup.py
@time: 2019/8/12 16:01
@function:
@inputParam:
@returnParam:
'''
import sqlite3
from getBackupInfo import getbackupObjectId,getbackupFieldKey
"""
      增加新的备份
      输入参数：objectList 
      格式：[(对象名，对象类型，备份开始时间，备份截止时间),()] 
      [('表1', 1,20190810,20190812), ('表2', 1,20190810,20190812), ('存储过程1', 2,20190810,20190812)] 
"""
def createBackup(objectList):
    tableList = []
    storedList = []
    viewList = []
    for list in objectList:
        if(list[1]==1):
            tableList.append(list)
        elif(list[1]==2):
            storedList.append(list)
        elif(list[1]==3):
            viewList.append(list)
    startId = getbackupObjectId()
    sqlite3Conn = sqlite3.connect('test.db')
    sqlite3Cursor = sqlite3Conn.cursor()
    for list in tableList:
        fieldList = getbackupFieldKey(list[0])[0]
        key = fieldList[1]
        fieldList = fieldList[0]
        fieldStr = ''
        for field in fieldList:
            fieldStr+= field[0]+','
        lenthField = len(fieldStr)
        fieldStr = field[0,lenthField-2]
        createSql = 'create table backup "%s" as select "%s" from "%s" WHERE time betwend "s%" and "s%"'\
                    %('backup'+str(startId),fieldStr,list[0],list[1],list[2])
        sqlite3Conn.execute(createSql)
        startId+=1

    sqlite3Conn.close()

lists = [('表1', 1,20190810,20190812), ('表2', 1,20190810,20190812), ('存储过程1', 2,20190810,20190812)]
createBackup(lists)

