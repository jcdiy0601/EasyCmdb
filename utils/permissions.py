#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django.shortcuts import render, redirect
from django.core.urlresolvers import resolve

perm_dic = {
    # 可以访问用户管理页面
    'cmdb_data.can_show_user': {
        'url_type': 0,       # 0代表相对路径，1代表绝对路径
        'url': 'user',       # url
        'method': 'GET',     # 请求方式
        'args': [],          # 请求参数
    },
    # 可以访问添加用户页面
    'cmdb_data.can_show_add_user': {
        'url_type': 0,
        'url': 'user_add',
        'method': 'GET',
        'args': []
    },
    # 可以添加用户
    'cmdb_data.can_add_user': {
        'url_type': 0,
        'url': 'user_add',
        'method': 'POST',
        'args': []
    },
    # 可以删除用户
    'cmdb_data.can_delete_user': {
        'url_type': 0,
        'url': 'delete_user_json',
        'method': 'POST',
        'args': []
    },
    # 可以访问用户编辑页面
    'cmdb_data.can_show_edit_user': {
        'url_type': 0,
        'url': 'user_edit',
        'method': 'GET',
        'args': []
    },
    # 可以编辑用户
    'cmdb_data.can_edit_user': {
        'url_type': 0,
        'url': 'user_edit',
        'method': 'POST',
        'args': []
    },
    # 可以访问重置密码页面
    'cmdb_data.can_show_change_pass_user': {
        'url_type': 0,
        'url': 'user_change_pass',
        'method': 'GET',
        'args': []
    },
    # 可以重置密码
    'cmdb_data.can_change_pass_user': {
        'url_type': 0,
        'url': 'user_change_pass',
        'method': 'POST',
        'args': []
    },
    # 可以访问修改用户权限页面
    'cmdb_data.can_show_change_permission_user': {
        'url_type': 0,
        'url': 'user_change_permission',
        'method': 'GET',
        'args': []
    },
    # 可以修改用户权限
    'cmdb_data.can_change_permission_user': {
        'url_type': 0,
        'url': 'user_change_permission',
        'method': 'POST',
        'args': []
    },
    # 可以访问业务线管理页面
    'cmdb_data.can_show_business_unit': {
        'url_type': 0,
        'url': 'business_unit',
        'method': 'GET',
        'args': []
    },
    # 可以更新业务线
    'cmdb_data.can_update_business_unit': {
        'url_type': 0,
        'url': 'update_business_unit_json',
        'method': 'POST',
        'args': []
    },
    # 可以删除业务线
    'cmdb_data.can_delete_business_unit': {
        'url_type': 0,
        'url': 'delete_business_unit_json',
        'method': 'POST',
        'args': []
    },
    # 可以访问添加业务线页面
    'cmdb_data.can_show_add_business_unit': {
        'url_type': 0,
        'url': 'business_unit_add',
        'method': 'GET',
        'args': []
    },
    # 可以添加业务线
    'cmdb_data.can_add_business_unit': {
        'url_type': 0,
        'url': 'business_unit_add',
        'method': 'POST',
        'args': []
    },
    # 可以访问IDC管理页面
    'cmdb_data.can_show_idc': {
        'url_type': 0,
        'url': 'idc',
        'method': 'GET',
        'args': []
    },
    # 可以更新IDC
    'cmdb_data.can_update_idc': {
        'url_type': 0,
        'url': 'update_idc_json',
        'method': 'POST',
        'args': []
    },
    # 可以删除IDC
    'cmdb_data.can_delete_idc': {
        'url_type': 0,
        'url': 'delete_idc_json',
        'method': 'POST',
        'args': []
    },
    # 可以访问添加IDC页面
    'cmdb_data.can_show_add_idc': {
        'url_type': 0,
        'url': 'idc_add',
        'method': 'GET',
        'args': []
    },
    # 可以添加IDC
    'cmdb_data.can_add_idc': {
        'url_type': 0,
        'url': 'idc_add',
        'method': 'POST',
        'args': []
    },
    # 可以访问标签管理页面
    'cmdb_data.can_show_tag': {
        'url_type': 0,
        'url': 'tag',
        'method': 'GET',
        'args': []
    },
    # 可以更新标签
    'cmdb_data.can_update_tag': {
        'url_type': 0,
        'url': 'update_tag_json',
        'method': 'POST',
        'args': []
    },
    # 可以删除标签
    'cmdb_data.can_delete_tag': {
        'url_type': 0,
        'url': 'delete_tag_json',
        'method': 'POST',
        'args': []
    },
    # 可以访问添加标签页面
    'cmdb_data.can_show_add_tag': {
        'url_type': 0,
        'url': 'tag_add',
        'method': 'GET',
        'args': []
    },
    # 可以添加标签
    'cmdb_data.can_add_tag': {
        'url_type': 0,
        'url': 'tag_add',
        'method': 'POST',
        'args': []
    },
    # 可以访问资产管理页面
    'cmdb_data.can_show_asset': {
        'url_type': 0,
        'url': 'asset',
        'method': 'GET',
        'args': []
    },
    # 可以更新资产
    'cmdb_data.can_update_asset': {
        'url_type': 0,
        'url': 'update_asset_json',
        'method': 'POST',
        'args': []
    },
    # 可以删除资产
    'cmdb_data.can_delete_asset': {
        'url_type': 0,
        'url': 'delete_asset_json',
        'method': 'POST',
        'args': []
    },
    # 可以访问资产详情页面
    'cmdb_data.can_show_asset_detail': {
        'url_type': 0,
        'url': 'asset_detail',
        'method': 'GET',
        'args': []
    },
    # 可以编辑硬盘转速
    'cmdb_data.can_change_speed_asset_detail': {
        'url_type': 0,
        'url': 'asset_detail_update_speed',
        'method': 'POST',
        'args': []
    },
    # 可以访问添加资产页面
    'cmdb_data.can_show_add_asset': {
        'url_type': 0,
        'url': 'asset_add',
        'method': 'GET',
        'args': []
    },
    # 可以访问添加硬件服务器资产
    'cmdb_data.can_show_add_hardware_server': {
        'url_type': 0,
        'url': 'asset_add_hardware_server',
        'method': 'GET',
        'args': []
    },
    # 可以访问添加软件服务器资产
    'cmdb_data.can_show_add_software_server': {
        'url_type': 0,
        'url': 'asset_add_software_server',
        'method': 'GET',
        'args': []
    },
    # 可以访问手工录入添加软件服务器资产
    'cmdb_data.can_show_hand_add_software_server': {
        'url_type': 0,
        'url': 'asset_hand_add_software_server',
        'method': 'GET',
        'args': []
    },
    # 可以添加硬件服务器资产
    'cmdb_data.can_add_hardware_server': {
        'url_type': 0,
        'url': 'asset_add_hardware_server',
        'method': 'POST',
        'args': []
    },
    # 可以添加软件服务器资产
    'cmdb_data.can_add_software_server': {
        'url_type': 0,
        'url': 'asset_add_software_server',
        'method': 'POST',
        'args': []
    },
    # 可以添加手工录入软件服务器资产
    'cmdb_data.can_hand_add_software_server': {
        'url_type': 0,
        'url': 'asset_hand_add_software_server',
        'method': 'POST',
        'args': []
    },
    # 可以访问资产编辑页面
    'cmdb_data.can_show_edit_asset': {
        'url_type': 0,
        'url': 'asset_edit',
        'method': 'GET',
        'args': []
    },
    # 可以编辑资产
    'cmdb_data.can_edit_asset': {
        'url_type': 0,
        'url': 'asset_edit',
        'method': 'POST',
        'args': []
    },
}


def perm_check(*args, **kwargs):
    """
    检查权限
    :param args:
    :param kwargs:
    :return:
    """
    request = args[0]
    if request.user.is_authenticated():     # 登录状态
        for permission_name, permission_info in perm_dic.items():
            url_matched = False
            if permission_info['url_type'] == 1:    # url为绝对路径
                if permission_info['url'] == request.path:  # 绝对路径匹配上了
                    url_matched = True
            else:   # url是相对路径，要把绝对的url请求转成相对的url name
                resolve_url_obj = resolve(request.path)
                current_url_name = resolve_url_obj.url_name
                if permission_info['url'] == current_url_name:  # 相对的url别名匹配上了
                    url_matched = True
            if url_matched:
                if permission_info['method'] == request.method:     # 请求方法也匹配上了
                    arg_matched = True
                    for request_arg in permission_info['args']:
                        request_method_func = getattr(request, permission_info['method'])
                        if not request_method_func.get(request_arg):
                            arg_matched = False
                    if arg_matched:     # 走到这里，仅仅代表这个请求和这条权限的定义规则匹配上了
                        if request.user.has_perm(permission_name):
                            return True     # 有权限
    else:
        redirect('/login.html')


def check_permission(func):
    """
    装饰器
    :param func:
    :return:
    """
    def inner(*args, **kwargs):
        request = args[0]
        if perm_check(*args, **kwargs) is True:
            return func(*args, **kwargs)
        else:
            return render(request, '403.html')
    return inner
