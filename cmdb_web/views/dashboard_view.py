#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django.contrib.auth.decorators import login_required
from utils.response import BaseResponse
from cmdb_data import models
from django.http import JsonResponse


@login_required
def chart1(request):
    """
    仪表盘图1视图
    :param request:
    :return:
    """
    response = BaseResponse()
    ret = {}
    asset_count = models.Asset.objects.all().count()
    idc_count = models.IDC.objects.all().count()
    business_unit_count = models.BusinessUnit.objects.all().count()
    tag_count = models.Tag.objects.all().count()
    user_count = models.UserProfile.objects.all().count()

    ret['asset_count'] = asset_count
    ret['idc_count'] = idc_count
    ret['business_unit_count'] = business_unit_count
    ret['tag_count'] = tag_count
    ret['user_count'] = user_count
    response.data = ret
    return JsonResponse(response.__dict__)


@login_required
def chart2(request):
    """
    仪表盘图2视图
    :param request:
    :return:
    """
    response = BaseResponse()
    ret = {}
    hardware_server_count = models.HardwareServer.objects.all().count()
    software_server_count = models.SoftwareServer.objects.all().count()
    network_device_count = models.NetworkDevice.objects.all().count()
    security_device_count = models.SecurityDevice.objects.all().count()
    ret['hardware_server_count'] = hardware_server_count
    ret['software_server_count'] = software_server_count
    ret['network_device_count'] = network_device_count
    ret['security_device_count'] = security_device_count
    response.data = ret
    return JsonResponse(response.__dict__)


@login_required
def chart3(request):
    """
        仪表盘图2视图
        :param request:
        :return:
        """
    response = BaseResponse()
    ret = {}
    hardware_server_count = models.HardwareServer.objects.all().count()
    software_server_count = models.SoftwareServer.objects.all().count()
    network_device_count = models.NetworkDevice.objects.all().count()
    security_device_count = models.SecurityDevice.objects.all().count()
    ret['hardware_server_count'] = hardware_server_count
    ret['software_server_count'] = software_server_count
    ret['network_device_count'] = network_device_count
    ret['security_device_count'] = security_device_count
    response.data = ret
    return JsonResponse(response.__dict__)
