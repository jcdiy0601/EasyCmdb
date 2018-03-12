#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from cmdb_web.service import user
from django.http import JsonResponse
from cmdb_web.forms import user_form
from cmdb_data import models
from utils.permissions import check_permission
from django.contrib.auth.models import Permission


@login_required
@check_permission
def user_page(request):
    """
    用户视图
    :param request:
    :return:
    """
    return render(request, 'user.html')


@login_required
def user_json(request):
    """
    获取用户数据视图
    :param request:
    :return:
    """
    obj = user.User()
    response = obj.fetch_user(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def delete_user_json(request):
    """
    删除用户视图
    :param request:
    :return:
    """
    response = user.User.delete_user(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def user_add(request):
    """
    添加用户视图
    :param request:
    :return:
    """
    if request.method == 'GET':
        form_obj = user_form.UserAddForm()
        return render(request, 'user_add.html', {'form_obj': form_obj})
    elif request.method == 'POST':
        form_obj = user_form.UserAddForm(request.POST)
        if form_obj.is_valid():
            email = form_obj.cleaned_data.get('email')
            name = form_obj.cleaned_data.get('name')
            password = form_obj.cleaned_data.get('password')
            phone = form_obj.cleaned_data.get('phone')
            user_obj = models.UserProfile.objects.create(email=email,
                                                         name=name,
                                                         phone=phone,
                                                         is_admin=False,
                                                         is_active=True,
                                                         is_superuser=False)
            user_obj.set_password(password)
            user_obj.save()
            return redirect('/cmdb_web/user.html')
        else:
            return render(request, 'user_add.html', {'form_obj': form_obj})


@login_required
@check_permission
def user_edit(request, *args, **kwargs):
    """
    编辑用户视图
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    user_id = kwargs['user_id']
    if request.method == 'GET':
        form_obj = user_form.UserEditForm(initial={'user_id': user_id})
        return render(request, 'user_edit.html', {'form_obj': form_obj, 'user_id': user_id})
    elif request.method == 'POST':
        form_obj = user_form.UserEditForm(data=request.POST, initial={'user_id': user_id})
        if form_obj.is_valid():
            user_obj = models.UserProfile.objects.get(id=user_id)
            user_obj.email = form_obj.cleaned_data.get('email')
            user_obj.name = form_obj.cleaned_data.get('name')
            user_obj.phone = form_obj.cleaned_data.get('phone')
            user_obj.save()
            return redirect('/cmdb_web/user.html')
        else:
            return render(request, 'user_edit.html', {'form_obj': form_obj, 'user_id': user_id})


@login_required
@check_permission
def user_change_pass(request, *args, **kwargs):
    """
    修改用户密码视图
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    user_id = kwargs['user_id']
    if request.method == 'GET':
        form_obj = user_form.UserChangePass()
        return render(request, 'user_change_pass.html', {'form_obj': form_obj, 'user_id': user_id})
    elif request.method == 'POST':
        form_obj = user_form.UserChangePass(request.POST)
        if form_obj.is_valid():
            password = form_obj.cleaned_data.get('password')
            user_obj = models.UserProfile.objects.get(id=user_id)
            user_obj.set_password(password)
            user_obj.save()
            return redirect('/cmdb_web/user.html')
        else:
            return render(request, 'user_change_pass.html', {'form_obj': form_obj, 'user_id': user_id})


@login_required
@check_permission
def user_change_permission(request, *args, **kwargs):
    """
    修改用户权限视图
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    user_id = kwargs['user_id']
    user_obj = models.UserProfile.objects.get(id=user_id)
    all_permission_list = list(Permission.objects.values('id', 'name'))
    user_permission_list = list(user_obj.user_permissions.values('id', 'name'))
    sub_permission_list = []
    for item in all_permission_list:
        if item not in user_permission_list:
            sub_permission_list.append(item)
    if request.method == 'POST':
        try:
            permission_list = request.POST.getlist('permission')
            user_obj.user_permissions.set(permission_list)
            return redirect('/cmdb_web/user.html')
        except Exception as e:
            error = str(e)
            return render(request, 'user_change_permission.html', {'user_id': user_id,
                                                                   'sub_permission_list': sub_permission_list,
                                                                   'user_permission_list': user_permission_list,
                                                                   'error': error})
    elif request.method == 'GET':
        return render(request, 'user_change_permission.html', {'user_id': user_id,
                                                               'sub_permission_list': sub_permission_list,
                                                               'user_permission_list': user_permission_list})