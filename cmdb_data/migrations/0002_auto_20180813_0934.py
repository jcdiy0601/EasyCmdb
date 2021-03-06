# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-08-13 01:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asset',
            options={'permissions': (('can_show_asset', '可以访问资产管理页面'), ('can_update_asset', '可以更新资产'), ('can_delete_asset', '可以删除资产'), ('can_show_asset_detail', '可以访问资产详情页面'), ('can_change_speed_asset_detail', '可以编辑硬盘转速'), ('can_show_add_asset', '可以访问添加资产页面'), ('can_show_add_hardware_server', '可以访问添加硬件服务器资产页面'), ('can_show_add_software_server', '可以访问添加软件件服务器资产页面'), ('can_show_add_network_device', '可以访问添加网络设备资产页面'), ('can_show_hand_add_security_device', '可以访问添加手工录入安全设备资产页面'), ('can_show_hand_add_software_server', '可以访问添加手工录入软件服务器资产页面'), ('can_add_hardware_server', '可以添加硬件服务器资产'), ('can_add_software_server', '可以添加软件服务器资产'), ('can_add_network_device', '可以添加网络设备资产'), ('can_hand_add_security_device', '可以添加手工录入安全设备资产'), ('can_hand_add_software_server', '可以添加手工录入软件服务器资产'), ('can_show_edit_asset', '可以访问资产编辑页面'), ('can_edit_asset', '可以编辑资产')), 'verbose_name_plural': '资产表'},
        ),
    ]
