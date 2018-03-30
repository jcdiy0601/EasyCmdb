# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-30 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_data', '0014_auto_20180330_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkdevice',
            name='device_type',
            field=models.CharField(choices=[('switch', '交换机'), ('firewall', '防火墙')], default='switch', max_length=64, verbose_name='设备类型'),
        ),
    ]