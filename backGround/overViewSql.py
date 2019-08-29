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
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
fp = logging.FileHandler('log.txt', encoding='utf-8')
fs = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])    # 调用

'''
返回分模块的对比结果差异
'''
def getModuleResult():
    contrastInfo = getCurContrastInfo()
    if len(contrastInfo)==0:
        return []
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
