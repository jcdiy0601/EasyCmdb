#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django import forms
from django.forms import fields
from django.forms import widgets
from cmdb_data import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class TagUpdateJsonForm(forms.Form):
    """
    ajax提交更新标签视图表单验证类
    """
    name = fields.CharField(
        max_length=64,
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
            'max_length': '最大长度不能大于64位'
        }
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        tag_obj = models.Tag.objects.filter(name=name).first()
        if tag_obj:
            raise ValidationError(_('标签%(name)s已存在'), code='invalid', params={'name': name})
        else:
            return self.cleaned_data.get('name')


class TagAddForm(forms.Form):
    """
    添加资产标签视图表单验证类
    """
    name = fields.CharField(
        max_length=64,
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
            'max_length': '最大长度不能大于64位'
        },
        label='标签名称',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        tag_obj = models.Tag.objects.filter(name=name).first()
        if tag_obj:
            raise ValidationError(_('标签%(name)s已存在'), code='invalid', params={'name': name})
        else:
            return self.cleaned_data.get('name')
