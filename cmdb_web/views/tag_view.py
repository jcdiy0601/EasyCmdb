#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from cmdb_web.service import tag
from django.http import JsonResponse
from cmdb_web.forms import tag_form
from cmdb_data import models
from utils.permissions import check_permission


@login_required
@check_permission
def tag_page(request):
    """
    标签视图
    :param request:
    :return:
    """
    return render(request, 'tag.html')


@login_required
def tag_json(request):
    """
    获取标签数据视图
    :param request:
    :return:
    """
    obj = tag.Tag()
    response = obj.fetch_tag(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def update_tag_json(request):
    """
    更新标签视图
    :param request:
    :return:
    """
    response = tag.Tag.update_tag(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def delete_tag_json(request):
    """
    删除标签视图
    :param request:
    :return:
    """
    response = tag.Tag.delete_tag(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def tag_add(request):
    """
    添加标签视图
    :param request:
    :return:
    """
    if request.method == 'GET':
        form_obj = tag_form.TagAddForm()
        return render(request, 'tag_add.html', {'form_obj': form_obj})
    elif request.method == 'POST':
        form_obj = tag_form.TagAddForm(request.POST)
        if form_obj.is_valid():
            name = form_obj.cleaned_data.get('name')
            models.Tag.objects.create(name=name, creator=request.user)
            return redirect('/cmdb_web/tag.html')
        else:
            return render(request, 'tag_add.html', {'form_obj': form_obj})
