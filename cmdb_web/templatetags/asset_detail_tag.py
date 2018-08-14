#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def display_asset_type(asset_obj):
    """
    显示资产类型
    :param asset_obj:
    :return:
    """
    choices = asset_obj.asset_type_choices
    asset_type = asset_obj.asset_type
    for item in choices:
        if item[0] == asset_type:
            asset_type = item[1]
            break
    return mark_safe(asset_type)


@register.simple_tag
def display_asset_status(asset_obj, asset_status_id):
    """
    显示资产状态
    :param asset_obj:
    :param asset_status_id:
    :return:
    """
    asset_status = None
    asset_status_choices = asset_obj.asset_status_choices
    for item in asset_status_choices:
        if item[0] == asset_status_id:
            asset_status = item[1]
            break
    return mark_safe(asset_status)


@register.simple_tag
def display_asset_auto(asset_obj):
    """
    显示资产是否为自动采集
    :param asset_obj:
    :return:
    """
    auto = asset_obj.auto
    if auto is True:
        return mark_safe('自动采集')
    else:
        return mark_safe('手工录入')


@register.simple_tag
def display_hardware_server_asset_nic(asset_obj):
    """
    显示硬件服务器网卡信息
    :param asset_obj:
    :return:
    """
    temp = ''
    for item in asset_obj.nic_set.all().order_by('slot'):
        temp = temp + '<tr>'
        temp = temp + '<td>' + item.slot + '</td>'
        temp = temp + '<td colspan="5">' + item.macaddress + '</td>'
        temp = temp + '</tr>'
    return mark_safe(temp)


@register.simple_tag
def display_software_server_asset_nic(asset_obj):
    """
    显示软件服务器网卡信息
    :param asset_obj:
    :return:
    """
    temp = ''
    for item in asset_obj.nic_set.all().order_by('name'):
        temp = temp + '<tr>'
        temp = temp + '<td>' + item.name + '</td>'
        temp = temp + '<td colspan="2">' + item.ipaddress + '</td>'
        temp = temp + '<td colspan="2">' + item.macaddress + '</td>'
        temp = temp + '</tr>'
    return mark_safe(temp)


@register.simple_tag
def display_hardware_server_asset_disk(asset_obj):
    """
    显示硬件服务器硬盘信息
    :param asset_obj:
    :return:
    """
    temp = ''
    for item in asset_obj.disk_set.all().order_by('slot'):
        temp = temp + '<tr>'
        temp = temp + '<td>' + item.slot + '</td>'
        temp = temp + '<td>' + item.sn + '</td>'
        temp = temp + '<td>' + item.manufacturer + '</td>'
        temp = temp + '<td>' + item.model + '</td>'
        temp = temp + '<td>' + '%s千转/分' % str(item.speed) + '<button type="button" nid="%s" class="change-speed btn btn-xs btn-default">编辑</button></td>' % item.id
        temp = temp + '<td>' + '%sG' % str(item.capacity) + '</td>'
        temp = temp + '</tr>'
    return mark_safe(temp)


@register.simple_tag
def display_hardware_server_asset_ram(asset_obj):
    """
    显示硬件服务器内存信息
    :param asset_obj:
    :return:
    """
    temp = ''
    for item in asset_obj.ram_set.all().order_by('slot'):
        temp = temp + '<tr>'
        temp = temp + '<td>' + item.slot + '</td>'
        temp = temp + '<td>' + item.sn + '</td>'
        temp = temp + '<td>' + item.manufacturer + '</td>'
        temp = temp + '<td>' + item.model + '</td>'
        temp = temp + '<td>' + '%s兆赫兹' % str(item.speed) + '</td>'
        temp = temp + '<td>' + '%sM' % str(item.capacity) + '</td>'
        temp = temp + '</tr>'
    return mark_safe(temp)


@register.simple_tag
def display_hardware_server_manufacturer(asset_obj, manufacturer_id):
    """显示硬件服务器主板厂商"""
    manufacturer = ''
    for item in asset_obj.hardwareserver.manufacturer_choices:
        if item[0] == manufacturer_id:
            manufacturer = item[1]
            break
    return mark_safe(manufacturer)


@register.simple_tag
def display_network_device_device_type(asset_obj, device_type_id):
    """显示网络设备设备类型"""
    device_type = ''
    for item in asset_obj.networkdevice.device_type_choices:
        if item[0] == device_type_id:
            device_type = item[1]
            break
    return mark_safe(device_type)


@register.simple_tag
def display_security_device_device_type(asset_obj, device_type_id):
    """显示安全设备设备类型"""
    device_type = ''
    for item in asset_obj.securitydevice.device_type_choices:
        if item[0] == device_type_id:
            device_type = item[1]
            break
    return mark_safe(device_type)


@register.simple_tag
def display_network_device_manufacturer(asset_obj, manufacturer_id):
    """显示网络设备厂商"""
    manufacturer = ''
    for item in asset_obj.networkdevice.manufacturer_choices:
        if item[0] == manufacturer_id:
            manufacturer = item[1]
            break
    return mark_safe(manufacturer)


@register.simple_tag
def display_security_device_manufacturer(asset_obj, manufacturer_id):
    """显示安全设备厂商"""
    manufacturer = ''
    for item in asset_obj.securitydevice.manufacturer_choices:
        if item[0] == manufacturer_id:
            manufacturer = item[1]
            break
    return mark_safe(manufacturer)