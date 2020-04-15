#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 18:23
# @Author  : QS
# @File    : identity_check.py
'''
检查登录状态
- 接收一个整数列表group
    - 包含012 (分别代表财务，采购，销售员)，以此赋予方法的使用权限，
'''
from django.shortcuts import redirect
from functools import wraps

def check(group):
    def decorator(func):

        def wra(req,*arg,**kwargs):
            identity = req.session.get('identity')
            if not identity:
                return redirect("/login/")
            if int(identity) not in group:
                return redirect("/login/")
            return func(req,*arg,**kwargs)
        return wra
    return decorator