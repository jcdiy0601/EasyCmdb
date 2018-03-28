#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from utils.response import BaseResponse
from cmdb_data import models
import traceback


def get_untreated_servers():
    """
    获取在线的硬件服务器、网络设备信息
    :return:
    """
    response = BaseResponse()
    response.data = {}
    try:
        hardware_server_objs = models.HardwareServer.objects.filter(asset__asset_status='online').all()
        for item in hardware_server_objs:
            response.data[item.manager_ip] = {
                'device_type': 'server',
                'manufacturer': item.manufacturer,
            }
        network_device_objs = models.NetworkDevice.objects.filter(asset__asset_status='online').all()
        for item in network_device_objs:
            response.data[item.manager_ip] = {
                'device_type': item.device_type,
                'manufacturer': item.manufacturer,
            }
    except Exception as e:
        response.message = str(e)
        response.status = False
        models.ErrorLog.objects.create(asset=None, title='get_untreated_servers', content=traceback.format_exc())
    return response
