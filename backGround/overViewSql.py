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
from backGround.contrast import getCurContrastInfo
'''
返回分模块的对比结果差异
'''
def getModuleResult():
    contrastInfo = getCurContrastInfo()
    contrastVersion = contrastInfo[0]
    contrastTableResult = contrastInfo[5]
    moduleList = getModuleInfo()
    changeModuleTableDict = {}
    changeModuleProcedureDict = {}
    changeModuleViewDict = {}
    for module in moduleList:
        tableList =  getObjectByModule(module)[0]
        changeTableList = []
        for table in tableList:
            table = table.upper()
            if table in contrastTableResult:
                if contrastTableResult[table][0]|contrastTableResult[table][1]|contrastTableResult[table][3]:
                    changeTableList.append(table)
        if len(changeTableList)!=0:
            changeModuleTableDict[module] = changeTableList
            changeModuleProcedureDict[module] = []
            changeModuleViewDict[module] = []
    return [contrastVersion,changeModuleTableDict,changeModuleProcedureDict,changeModuleViewDict]
print(getModuleResult())
