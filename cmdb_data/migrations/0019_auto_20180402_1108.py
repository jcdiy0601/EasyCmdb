# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-02 03:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_data', '0018_auto_20180402_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessunit',
            name='memo',
        ),
        migrations.RemoveField(
            model_name='idc',
            name='memo',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='memo',
        ),
    ]