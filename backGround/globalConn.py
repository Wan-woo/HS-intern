#!/usr/bin/env python
# encoding: utf-8
'''
@author: zwd
@contact: zwdeng@163.com
@file: globalConn.py
@time: 2019/8/9 11:01
@function:
@inputParam:
@returnParam:
'''
def _init():
    global _global_dict
    _global_dict = {'userName':'zwd','passWord':'123456','host':'192.168.230.187','serviceName':'orcl.hs.handsome.com.cn'}

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue
