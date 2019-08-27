#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: addFieldScript.py
@time: 2019/8/23 15:51
@function:获取字段并插入
@inputParam:
@returnParam:
'''
from backGround.setupSql import getOracleInfo,tuplesToList,listsToList
from backGround.testConnection import sqliteExecute,oracleExcute

[tableList,produceList,viewList,fieldDicts] = getOracleInfo()
tableList = sqliteExecute("select distinct(tableName) from backupFieldKey   ")
tableList = tuplesToList(tableList)
tableList = listsToList(tableList)
for table in tableList:
    try:
        fieldList = fieldDicts[table]
        for field in fieldList:
            insertSql= "insert into backupFieldKey (tableName,fieldChosed,fieldType,isSystemDefine) values " \
                       "('%s','%s','1','1')"%(table,field)
            sqliteExecute(insertSql)
    except Exception as err:
        print(table+"不存在")
