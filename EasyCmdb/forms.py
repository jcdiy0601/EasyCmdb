#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class AccloginForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required': '邮箱不能为空', 'invalid': '格式错误'}
    )
    password = forms.CharField(
        max_length=128,
        error_messages={'required': '密码不能为空', 'max_length': '密码长度不能大于128位'}
    )


class UserInfoForm(forms.Form):
    password1 = forms.CharField(
        max_length=128,
        error_messages={'required': '密码不能为空', 'max_length': '密码长度不能大于128位'}
    )
    password2 = forms.CharField(
        max_length=128,
        error_messages={'required': '密码不能为空', 'max_length': '密码长度不能大于128位'}
    )

    def clean(self):
        if self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data
        else:
            raise ValidationError("两次输入的密码不一致")
