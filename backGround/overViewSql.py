#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: overViewSql.py
@time: 2019/8/26 15:04
@function:
@inputParam:
@returnParam:
'''
from backGround.setupSql import getModuleInfo,getObjectByModule
from backGround.contrast import getCurContrasrInfo
'''
返回分模块的对比结果差异
'''
def getModuleResult():
    contrasrInfo = getCurContrasrInfo()
    contrasrVersion = contrasrInfo[0]
    contrasrTableResult = contrasrInfo[5]
    moduleList = getModuleInfo()
    changeModuleTableDict = {}
    for module in moduleList:
        tableList =  getObjectByModule(module)[0]
        changeTableList = []
        for table in tableList:
            table = table.upper()
            if table in contrasrTableResult:
                if contrasrTableResult[table][0]|contrasrTableResult[table][1]|contrasrTableResult[table][3]:
                    changeTableList.append(table)
        if len(changeTableList)!=0:
            changeModuleTableDict[module] = changeTableList
    return [contrasrVersion,changeModuleTableDict]
print(getModuleResult())
