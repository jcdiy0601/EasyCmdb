#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cmdb_data import models
from utils.response import BaseResponse


@login_required
def show_all_affiliation(request):
    """
    显示所有软件服务器归属
    :param request:
    :return:
    """
    software_server_obj_list = models.SoftwareServer.objects.all()
    result = {}
    for software_server_obj in software_server_obj_list:
        if len(software_server_obj.hostname.split('_')) != 2:
            continue
        esxi_ip = software_server_obj.hostname.split('_')[-1]
        if esxi_ip not in result:
            result[esxi_ip] = []
        nic_obj = models.NIC.objects.get(asset=software_server_obj.asset)
        result[esxi_ip].append(nic_obj.ipaddress)
    return render(request, 'show_all_affiliation.html', {'result': result})


@login_required
def search_affiliation(request):
    """
    查询软件服务器归属
    :param request:
    :return:
    """
    response = BaseResponse()
    if request.method == 'POST':
        ret = {}
        ip_str = request.POST.get('ip').strip()
        ip_str = ip_str.replace('，', ',')
        ip_list = ip_str.split(',')
        for ip in ip_list:
            nic_obj = models.NIC.objects.filter(ipaddress=ip).first()
            if nic_obj:
                software_server_obj = models.SoftwareServer.objects.filter(asset=nic_obj.asset).first()
                esxi_ip = software_server_obj.hostname.split('_')[-1]
                ret[ip] = esxi_ip
            else:
                ret[ip] = '不存在'
        response.data = ret
        return JsonResponse(response.__dict__)
    return render(request, 'search_affiliation.html')
