#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django import forms
from django.forms import fields
from django.forms import widgets
from cmdb_data import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class BusinessUnitUpdateJsonForm(forms.Form):
    """
    ajax提交更新业务线视图表单验证类
    """
    name = fields.CharField(
        max_length=64,
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
            'max_length': '最大长度不能大于64位'
        }
    )
    contact_id = fields.IntegerField(
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
        }
    )
    manager = fields.IntegerField(
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
        }
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        n = models.BusinessUnit.objects.filter(name=self.cleaned_data.get('name')).count()
        if not n:
            return self.cleaned_data.get('name')
        else:
            raise ValidationError(_('业务线%(name)s已存在'), code='invalid', params={'name': name})

    def clean_contacts_id(self):
        c = models.UserProfile.objects.filter(id=self.cleaned_data.get('contacts_id')).count()
        if c:
            return self.cleaned_data.get('contacts_id')
        else:
            raise ValidationError(_('联系人不存在'), code='invalid')

    def clean_managers_id(self):
        m = models.UserProfile.objects.filter(id=self.cleaned_data.get('managers_id')).count()
        if m:
            return self.cleaned_data.get('managers_id')
        else:
            raise ValidationError(_('管理人不存在'), code='invalid')


class BusinessUnitAddForm(forms.Form):
    """
    添加资产业务线视图表单验证类
    """
    name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='业务线名称',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    contact_id = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='联系人',
        help_text='必填项',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control',
                   'placeholder': '联系人'}
        )
    )
    manager_id = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='管理人',
        help_text='必填项',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control',
                   'placeholder': '管理人'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(BusinessUnitAddForm, self).__init__(*args, **kwargs)
        self.fields['contact_id'].widget.choices = models.UserProfile.objects.values_list('id', 'name')
        self.fields['manager_id'].widget.choices = models.UserProfile.objects.values_list('id', 'name')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        n = models.BusinessUnit.objects.filter(name=self.cleaned_data.get('name')).count()
        if not n:
            return self.cleaned_data.get('name')
        else:
            raise ValidationError(_('业务线%(name)s已存在'), code='invalid', params={'name': name})

    def clean_contact_id(self):
        c = models.UserProfile.objects.filter(id=self.cleaned_data.get('contact_id')).count()
        if c:
            return self.cleaned_data.get('contact_id')
        else:
            raise ValidationError(_('联系人不存在'), code='invalid')

    def clean_manager_id(self):
        m = models.UserProfile.objects.filter(id=self.cleaned_data.get('manager_id')).count()
        if m:
            return self.cleaned_data.get('manager_id')
        else:
            raise ValidationError(_('管理人不存在'), code='invalid')
