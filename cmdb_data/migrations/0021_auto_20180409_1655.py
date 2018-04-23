# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-09 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_data', '0020_auto_20180402_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardwareserver',
            name='manufacturer',
            field=models.CharField(choices=[('dell', 'DELL')], default='dell', max_length=64, verbose_name='厂商'),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='manufacturer',
            field=models.CharField(choices=[('h3c', 'H3C'), ('juniper', 'Juniper')], default='h3c', max_length=64, verbose_name='厂商'),
        ),
    ]