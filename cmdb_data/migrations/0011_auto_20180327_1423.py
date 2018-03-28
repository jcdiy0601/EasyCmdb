# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-27 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_data', '0010_auto_20180327_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardwareserver',
            name='manufacturer',
            field=models.CharField(choices=[('dell', '戴尔')], default='dell', max_length=64, verbose_name='制造商'),
        ),
    ]