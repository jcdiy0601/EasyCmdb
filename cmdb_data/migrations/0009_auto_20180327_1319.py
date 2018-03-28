# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-27 05:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_data', '0008_auto_20180327_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkdevice',
            name='device_type',
            field=models.CharField(choices=[('switch', '交换机')], default='switch', max_length=64, verbose_name='设备类型'),
        ),
        migrations.AlterField(
            model_name='hardwareserver',
            name='manufacturer',
            field=models.CharField(choices=[('dell', '戴尔')], default='dell', max_length=64, verbose_name='制造商'),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='manufacturer',
            field=models.CharField(choices=[('h3c', '华三')], default='h3c', max_length=64, verbose_name='制造商'),
        ),
    ]