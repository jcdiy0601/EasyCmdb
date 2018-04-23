#!/usr/bin/env python
# Author: 'JiaChen'

from cmdb_data import models
from utils.response import BaseResponse


def check_softwareserver_exist(hostname):
    """查看软件服务器是否存在"""
    response = BaseResponse()
    host_obj = models.SoftwareServer.objects.filter(hostname=hostname).first()
    if host_obj:
        response.status = False
        response.message = '此软件服务器的主机名已存在'
    else:
        response.message = '此软件服务器的主机名不存在，可以使用'
    return response
