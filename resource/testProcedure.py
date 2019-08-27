#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: testProcedure.py
@time: 2019/8/26 18:54
@function:测试存储过程
@inputParam:
@returnParam:
'''

from backGround.setupSql import getOracleInfo,tuplesToList,listsToList
from backGround.testConnection import getOrcaleConnection
[tableList,procedureNameList,viewList,fieldDicts]= getOracleInfo()
oracleConn = getOrcaleConnection()
oracleCursor = oracleConn.cursor()
procedureList = []
for procedure in procedureNameList:
    sql = "SELECT text FROM user_source   WHERE NAME = '%s' ORDER BY line"%(procedure)
    oracleCursor.execute(sql)
    procedureTextList = tuplesToList(oracleCursor.fetchall())
    procedureTextList = listsToList(procedureTextList)
    procedureText = ''.join(procedureTextList)
    procedureText = procedureText.replace('\n','')
    procedureList.append(procedureText)
oracleConn.close()
print(procedureList)
