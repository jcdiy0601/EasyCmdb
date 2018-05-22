#!/usr/bin/env python
# Author: 'JiaChen'

from cmdb_data import models
from utils.response import BaseResponse


def check_hostname_exit(hostname):
    """
    检查主机名是否存在
    :param hostname:
    :return:
    """
    response = BaseResponse()
    host_obj = models.SoftwareServer.objects.filter(hostname=hostname).first()
    if host_obj:
        response.message = '此软件服务器的主机名不存在，可以使用'
    else:
        response.status = False
        response.message = '此软件服务器的主机名已存在'
    return response
