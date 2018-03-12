#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from cmdb_web.service import idc
from django.http import JsonResponse
from cmdb_web.forms import idc_form
from cmdb_data import models
from utils.permissions import check_permission


@login_required
@check_permission
def idc_page(request):
    """
    IDC视图
    :param request:
    :return:
    """
    return render(request, 'idc.html')


@login_required
def idc_json(request):
    """
    获取IDC数据视图
    :param request:
    :return:
    """
    obj = idc.Idc()
    response = obj.fetch_idc(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def update_idc_json(request):
    """
    更新IDC视图
    :param request:
    :return:
    """
    response = idc.Idc.update_idc(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def delete_idc_json(request):
    """
    删除IDC视图
    :param request:
    :return:
    """
    response = idc.Idc.delete_idc(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def idc_add(request):
    """
    添加IDC视图
    :param request:
    :return:
    """
    if request.method == 'GET':
        form_obj = idc_form.IdcAddForm()
        return render(request, 'idc_add.html', {'form_obj': form_obj})
    elif request.method == 'POST':
        form_obj = idc_form.IdcAddForm(request.POST)
        if form_obj.is_valid():
            models.IDC.objects.create(**form_obj.cleaned_data)
            return redirect('/cmdb_web/idc.html')
        else:
            return render(request, 'idc_add.html', {'form_obj': form_obj})
