#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django import forms
from django.forms import fields
from django.forms import widgets
from cmdb_data import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class IdcUpdateJsonForm(forms.Form):
    """
    ajax提交更新IDC视图表单验证类
    """
    name = fields.CharField(
        max_length=64,
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
            'max_length': '最大长度不能大于64位'
        }
    )
    floor = fields.IntegerField(
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
        }
    )

    def clean(self):
        name = self.cleaned_data.get('name')
        floor = self.cleaned_data.get('floor')
        idc_obj = models.IDC.objects.filter(name=name, floor=floor).first()
        if idc_obj:
            raise ValidationError(_('机房%(name)s楼层%(floor)s已存在'), code='invalid', params={'name': name, 'floor': floor})
        else:
            return self.cleaned_data


class IdcAddForm(forms.Form):
    """
    添加资产IDC视图表单验证类
    """
    name = fields.CharField(
        max_length=64,
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
            'max_length': '最大长度不能大于64位'
        },
        label='IDC机房',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    floor = fields.IntegerField(
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
        },
        label='楼层',
        help_text='必填项',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean(self):
        name = self.cleaned_data.get('name')
        floor = self.cleaned_data.get('floor')
        idc_obj = models.IDC.objects.filter(name=name, floor=floor).first()
        if idc_obj:
            raise ValidationError(_('机房%(name)s楼层%(floor)s已存在'), code='invalid', params={'name': name, 'floor': floor})
        else:
            return self.cleaned_data
