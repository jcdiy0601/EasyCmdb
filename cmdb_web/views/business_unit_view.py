#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from cmdb_web.service import business_unit
from django.http import JsonResponse
from cmdb_web.forms import business_unit_form
from cmdb_data import models
from utils.permissions import check_permission


@login_required
@check_permission
def business_unit_page(request):
    """
    业务线视图
    :param request:
    :return:
    """
    return render(request, 'business_unit.html')


@login_required
def business_unit_json(request):
    """
    获取业务线数据视图
    :param request:
    :return:
    """
    obj = business_unit.BusinessUnit()
    response = obj.fetch_business_unit(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def update_business_unit_json(request):
    """
    更新业务线视图
    :param request:
    :return:
    """
    response = business_unit.BusinessUnit.update_business_unit(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def delete_business_unit_json(request):
    """
    删除业务线视图
    :param request:
    :return:
    """
    response = business_unit.BusinessUnit.delete_business_unit(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def business_unit_add(request):
    """
    添加业务线视图
    :param request:
    :return:
    """
    if request.method == 'GET':
        form_obj = business_unit_form.BusinessUnitAddForm()
        return render(request, 'business_unit_add.html', {'form_obj': form_obj})
    elif request.method == 'POST':
        form_obj = business_unit_form.BusinessUnitAddForm(request.POST)
        if form_obj.is_valid():
            models.BusinessUnit.objects.create(**form_obj.cleaned_data)
            return redirect('/cmdb_web/business_unit.html')
        else:
            return render(request, 'business_unit_add.html', {'form_obj': form_obj})
