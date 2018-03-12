#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils.task_search_ip import SearchIp
from utils.response import BaseResponse
from django.http import JsonResponse
from utils.ip_sort import ip_sort
import IPy
import re


@login_required
def search_ip(request):
    """
    查询可用IP视图
    :param request:
    :return:
    """
    return render(request, 'search_ip.html')


@login_required
def search_ip_json(request):
    """
    获取可用IP数据视图
    :param request:
    :return:
    """
    response = BaseResponse()
    if request.method == 'POST':
        ip = request.POST.get('ip').strip()
        res = re.search('\d+.\d+.\d+.0/\d+', ip)
        if res:
            ip_list = IPy.IP(ip)
            obj = SearchIp(ip_list)
            available_ip_list = obj.process()
            available_ip_list = ip_sort(available_ip_list)
            response.data = available_ip_list
            return JsonResponse(response.__dict__)
        else:
            response.status = False
            response.message = '输入的不是一个正确的网段'
            return JsonResponse(response.__dict__)
