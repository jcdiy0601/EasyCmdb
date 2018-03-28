# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-27 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_data', '0006_auto_20180223_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=64, unique=True, verbose_name='SN号')),
                ('manager_ip', models.GenericIPAddressField(unique=True, verbose_name='管理IP')),
                ('port_number', models.IntegerField(blank=True, null=True, verbose_name='接口数')),
                ('run_time', models.IntegerField(blank=True, null=True, verbose_name='运行时常')),
                ('device_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='设备名称')),
                ('manufacturer', models.CharField(blank=True, max_length=64, null=True, verbose_name='制造商')),
                ('model', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('basic_info', models.CharField(blank=True, max_length=128, null=True, verbose_name='基本信息')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('latest_date', models.DateField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name_plural': '网络设备表',
            },
        ),
        migrations.AlterModelOptions(
            name='asset',
            options={'permissions': (('can_show_asset', '可以访问资产管理页面'), ('can_update_asset', '可以更新资产'), ('can_delete_asset', '可以删除资产'), ('can_show_asset_detail', '可以访问资产详情页面'), ('can_change_speed_asset_detail', '可以编辑硬盘转速'), ('can_show_add_asset', '可以访问添加资产页面'), ('can_show_add_hardware_server', '可以访问添加硬件服务器资产页面'), ('can_show_add_software_server', '可以访问添加软件件服务器资产页面'), ('can_show_add_network_device', '可以访问添加网络设备资产页面'), ('can_show_hand_add_software_server', '可以访问添加手工录入软件服务器资产页面'), ('can_add_hardware_server', '可以添加硬件服务器资产'), ('can_add_software_server', '可以添加软件服务器资产'), ('can_add_network_device', '可以添加网络设备资产'), ('can_hand_add_software_server', '可以添加手工录入软件服务器资产'), ('can_show_edit_asset', '可以访问资产编辑页面'), ('can_edit_asset', '可以编辑资产')), 'verbose_name_plural': '资产表'},
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='asset',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cmdb_data.Asset', verbose_name='所属资产'),
        ),
    ]
