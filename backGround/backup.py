#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: backup.py
@time: 2019/8/9 10:24
@function:
@inputParam:backupList 有四个字段 objectName objectType begintime endtime 备份的所有表使用相同的开始时间和结束时间
@returnParam:
'''

def backup(backupList):
    backupList1 = []
    backupList2 = []
    backupList3 = []
    if(len(backupList)==0):
        return
    begintime=backupList[0][2]
    endtime=backupList[0][3]

    for sublist in backupList:
        if(sublist[1]==1):
            backupList1.append(sublist[0])
        if(sublist[1]==2):
            backupList2.append(sublist[0])
        if(sublist[1]==3):
            backupList3.append(sublist[0])

