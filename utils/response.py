#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen


class BaseResponse(object):
    """
    初始化响应类
    """
    def __init__(self):
        self.status = True
        self.message = None
        self.data = None
        self.error = None
