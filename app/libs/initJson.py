#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 18:16
# @Author  : QS
# @File    : initJson.py

def initJson(success=True):
    if success:
        return {
            'code':200,  #代表成功
            'state':'success',
            'detail':'',
            }
    else:
        return {
            'code':400,  #代表失败
            'state':'error',
            'detail':'',
        }
