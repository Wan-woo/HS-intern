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
from getBackupInfo import getBackupTime,getObjectByVersion
def makeContrasr(backupVersion):
    [startTime,endTime]=getBackupTime(backupVersion)
    objectList = getObjectByVersion(backupVersion)

