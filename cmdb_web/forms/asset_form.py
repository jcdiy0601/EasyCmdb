#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from django import forms
from django.forms import fields
from django.forms import widgets
from cmdb_data import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class AssetUpdateJsonForm(forms.Form):
    """
    ajax提交更新资产视图表单验证类
    """
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'}
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'}
    )
    asset_status = fields.CharField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'}
    )


class AssetAddHardwareServerForm(forms.Form):
    """
    资产添加硬件服务器视图表单验证类
    """
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('hardwareserver', '硬件服务器')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    cabinet_num = fields.CharField(
        required=False,
        max_length=32,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于32位'},
        label='机柜号',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_begin_order = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='机柜起始序号(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_occupy_num = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='设备大小(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    manufacturer = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='厂商',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('dell', '戴尔')],
            attrs={'class': 'form-control'}
        )
    )
    sn = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='SN号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    manager_ip = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='管理IP',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    purchasing_company = fields.CharField(
        required=False,
        max_length=64,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='采购公司',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    trade_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='购买时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    expire_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='保修到期时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetAddHardwareServerForm, self).__init__(*args, **kwargs)
        business_unit_id_choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        business_unit_id_choices.insert(0, (None, ''))
        self.fields['business_unit_id'].widget.choices = business_unit_id_choices
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices

    def clean_sn(self):
        sn = self.cleaned_data.get('sn')
        n = models.HardwareServer.objects.filter(sn=sn).count()
        if not n:
            return self.cleaned_data.get('sn')
        else:
            raise ValidationError(_('SN号%(sn)s已存在'), code='invalid', params={'sn': sn})

    def clean_manager_ip(self):
        manager_ip = self.cleaned_data.get('manager_ip')
        n = models.HardwareServer.objects.filter(manager_ip=manager_ip).count()
        if not n:
            return self.cleaned_data.get('manager_ip')
        else:
            raise ValidationError(_('管理IP%(manager_ip)s已存在'),
                                  code='invalid',
                                  params={'manager_ip': manager_ip})


class AssetAddSoftwareServerForm(forms.Form):
    """
    资产添加软件服务器视图表单验证类
    """
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('softwareserver', '软件服务器')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    hostname = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='主机名',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetAddSoftwareServerForm, self).__init__(*args, **kwargs)
        business_unit_id_choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        business_unit_id_choices.insert(0, (None, ''))
        self.fields['business_unit_id'].widget.choices = business_unit_id_choices
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices

    def clean_hostname(self):
        hostname = self.cleaned_data.get('hostname')
        n = models.SoftwareServer.objects.filter(hostname=hostname).count()
        if not n:
            return self.cleaned_data.get('hostname')
        else:
            raise ValidationError(_('主机名%(hostname)s已存在'), code='invalid', params={'hostname': hostname})


class AssetHandAddSoftwareServerForm(forms.Form):
    """
    资产添加手工录入软件服务器视图表单验证类
    """
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('softwareserver', '软件服务器')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    hostname = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='主机名',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    os_version = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='系统版本',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cpu_model = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='CPU型号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cpu_physical_count = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='CPU物理个数',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cpu_count = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='CPU逻辑个数',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    ram_total_capacity = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='内存总大小(MB)',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    disk_total_capacity = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='磁盘总大小(GB)',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    nic_name = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='网卡名称',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    nic_macaddress = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='MAC',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    nic_ipaddress = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='IP',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetHandAddSoftwareServerForm, self).__init__(*args, **kwargs)
        business_unit_id_choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        business_unit_id_choices.insert(0, (None, ''))
        self.fields['business_unit_id'].widget.choices = business_unit_id_choices
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices

    def clean_hostname(self):
        hostname = self.cleaned_data.get('hostname')
        n = models.SoftwareServer.objects.filter(hostname=hostname).count()
        if not n:
            return self.cleaned_data.get('hostname')
        else:
            raise ValidationError(_('主机名%(hostname)s已存在'), code='invalid', params={'hostname': hostname})

    def clean_nic_macaddress(self):
        macaddress = self.cleaned_data.get('nic_macaddress')
        n = models.NIC.objects.filter(macaddress=macaddress).count()
        if not n:
            return self.cleaned_data.get('nic_macaddress')
        else:
            raise ValidationError(_('MAC%(macaddress)s已存在'), code='invalid', params={'macaddress': macaddress})


class AssetAddNetworkDeviceForm(forms.Form):
    """资产添加网络设备视图表单验证类"""
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('networkdevice', '网络设备')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    cabinet_num = fields.CharField(
        required=False,
        max_length=32,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于32位'},
        label='机柜号',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_begin_order = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='机柜起始序号(U)',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_occupy_num = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='设备大小(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    device_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='设备类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('switch', '交换机'), ('firewall', '防火墙')],
            attrs={'class': 'form-control'}
        )
    )
    manufacturer = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='厂商',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('h3c', '华三'), ('juniper', '瞻博')],
            attrs={'class': 'form-control'}
        )
    )
    sn = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='SN号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    manager_ip = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='管理IP',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    purchasing_company = fields.CharField(
        required=False,
        max_length=64,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='采购公司',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    trade_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='购买时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    expire_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='保修到期时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )

    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetAddNetworkDeviceForm, self).__init__(*args, **kwargs)
        business_unit_id_choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        business_unit_id_choices.insert(0, (None, ''))
        self.fields['business_unit_id'].widget.choices = business_unit_id_choices
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices

    def clean_sn(self):
        sn = self.cleaned_data.get('sn')
        n = models.NetworkDevice.objects.filter(sn=sn).count()
        if not n:
            return self.cleaned_data.get('sn')
        else:
            raise ValidationError(_('SN号%(sn)s已存在'), code='invalid', params={'sn': sn})

    def clean_manager_ip(self):
        manager_ip = self.cleaned_data.get('manager_ip')
        n = models.NetworkDevice.objects.filter(manager_ip=manager_ip).count()
        if not n:
            return self.cleaned_data.get('manager_ip')
        else:
            raise ValidationError(_('管理IP%(manager_ip)s已存在'),
                                  code='invalid',
                                  params={'manager_ip': manager_ip})


class AssetHandAddSecurityDeviceForm(forms.Form):
    """资产添加安全设备视图表单验证类"""
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('securitydevice', '安全设备')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    cabinet_num = fields.CharField(
        required=False,
        max_length=32,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于32位'},
        label='机柜号',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_begin_order = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='机柜起始序号(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_occupy_num = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='设备大小(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    device_name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='设备名称',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    device_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='设备类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('waf', 'WAF'), ('ads', 'ADS'), ('ips', 'IPS')],
            attrs={'class': 'form-control'}
        )
    )
    manufacturer = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='厂商',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('nsfocus', '绿盟')],
            attrs={'class': 'form-control'}
        )
    )
    sn = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='SN号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    manager_ip = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='管理IP',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    model = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='型号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    port_number = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='接口数',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    purchasing_company = fields.CharField(
        required=False,
        max_length=64,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='采购公司',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    trade_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='购买时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    expire_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='保修到期时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetHandAddSecurityDeviceForm, self).__init__(*args, **kwargs)
        business_unit_id_choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        business_unit_id_choices.insert(0, (None, ''))
        self.fields['business_unit_id'].widget.choices = business_unit_id_choices
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices

    def clean_sn(self):
        sn = self.cleaned_data.get('sn')
        n = models.NetworkDevice.objects.filter(sn=sn).count()
        if not n:
            return self.cleaned_data.get('sn')
        else:
            raise ValidationError(_('SN号%(sn)s已存在'), code='invalid', params={'sn': sn})

    def clean_manager_ip(self):
        manager_ip = self.cleaned_data.get('manager_ip')
        n = models.NetworkDevice.objects.filter(manager_ip=manager_ip).count()
        if not n:
            return self.cleaned_data.get('manager_ip')
        else:
            raise ValidationError(_('管理IP%(manager_ip)s已存在'),
                                  code='invalid',
                                  params={'manager_ip': manager_ip})


class AssetEditHardwareServerForm(forms.Form):
    """
    编辑资产硬件服务器视图表单验证类
    """
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('hardwareserver', '硬件服务器')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    cabinet_num = fields.CharField(
        required=False,
        max_length=32,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于32位'},
        label='机柜号',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_begin_order = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='机柜起始序号(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_occupy_num = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='设备大小(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    manufacturer = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='厂商',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('dell', '戴尔')],
            attrs={'class': 'form-control'}
        )
    )
    sn = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='SN号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    manager_ip = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='管理IP',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    purchasing_company = fields.CharField(
        required=False,
        max_length=64,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='采购公司',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    trade_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='购买时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    expire_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='保修到期时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetEditHardwareServerForm, self).__init__(*args, **kwargs)
        self.asset_id = self.initial['asset_id']
        self.fields['asset_type'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_type')
        for item in list(query_set):
            self.fields['asset_type'].initial.append(item['asset_type'])
        self.fields['business_unit_id'].widget.choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        self.fields['business_unit_id'].widget.choices.insert(0, (None, ''))
        self.fields['business_unit_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('business_unit_id')
        for item in list(query_set):
            self.fields['business_unit_id'].initial.append(item['business_unit_id'])
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        self.fields['tag_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('tag__id')
        for item in list(query_set):
            self.fields['tag_id'].initial.append(item['tag__id'])
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices
        self.fields['idc_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('idc_id')
        for item in list(query_set):
            self.fields['idc_id'].initial.append(item['idc_id'])
        self.fields['cabinet_num'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_num
        self.fields['cabinet_begin_order'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_begin_order
        self.fields['cabinet_occupy_num'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_occupy_num
        self.fields['purchasing_company'].initial = models.Asset.objects.filter(id=self.asset_id).first().purchasing_company
        self.fields['trade_date'].initial = models.Asset.objects.filter(id=self.asset_id).first().trade_date
        self.fields['expire_date'].initial = models.Asset.objects.filter(id=self.asset_id).first().expire_date
        self.fields['asset_status'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_status')
        for item in list(query_set):
            self.fields['asset_status'].initial.append(item['asset_status'])
        self.fields['manufacturer'].initial = []
        query_set = models.HardwareServer.objects.filter(asset_id=self.asset_id).values('manufacturer')
        for item in list(query_set):
            self.fields['manufacturer'].initial.append(item['manufacturer'])
        self.fields['sn'].initial = models.HardwareServer.objects.filter(asset_id=self.asset_id).first().sn
        self.fields['manager_ip'].initial = models.HardwareServer.objects.filter(asset_id=self.asset_id).first().manager_ip

        self.fields['memo'].initial = models.Asset.objects.filter(id=self.asset_id).first().memo

    def clean_sn(self):
        sn = self.cleaned_data.get('sn')
        n = models.HardwareServer.objects.exclude(asset_id=self.asset_id).filter(sn=self.cleaned_data.get('sn')).count()
        if not n:
            return self.cleaned_data.get('sn')
        else:
            raise ValidationError(_('SN号%(sn)s已存在'), code='invalid', params={'sn': sn})

    def clean_manager_ip(self):
        manager_ip = self.cleaned_data.get('manager_ip')
        n = models.HardwareServer.objects.exclude(asset_id=self.asset_id).filter(manager_ip=self.cleaned_data.get('manager_ip')).count()
        if not n:
            return self.cleaned_data.get('manager_ip')
        else:
            raise ValidationError(_('管理IP%(manager_ip)s已存在'), code='invalid', params={'manager_ip': manager_ip})


class AssetEditSoftwareServerForm(forms.Form):
    """
    编辑资产软件服务器视图表单验证类
    """
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('softwareserver', '软件服务器')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    hostname = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='主机名',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetEditSoftwareServerForm, self).__init__(*args, **kwargs)
        self.asset_id = self.initial['asset_id']
        self.fields['asset_type'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_type')
        for item in list(query_set):
            self.fields['asset_type'].initial.append(item['asset_type'])
        self.fields['business_unit_id'].widget.choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        self.fields['business_unit_id'].widget.choices.insert(0, (None, ''))
        self.fields['business_unit_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('business_unit_id')
        for item in list(query_set):
            self.fields['business_unit_id'].initial.append(item['business_unit_id'])
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        self.fields['tag_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('tag__id')
        for item in list(query_set):
            self.fields['tag_id'].initial.append(item['tag__id'])
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices
        self.fields['idc_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('idc_id')
        for item in list(query_set):
            self.fields['idc_id'].initial.append(item['idc_id'])
        self.fields['asset_status'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_status')
        for item in list(query_set):
            self.fields['asset_status'].initial.append(item['asset_status'])
        self.fields['hostname'].initial = models.SoftwareServer.objects.filter(asset_id=self.asset_id).first().hostname
        self.fields['memo'].initial = models.Asset.objects.filter(id=self.asset_id).first().memo

    def clean_hostname(self):
        hostname = self.cleaned_data.get('hostname')
        n = models.SoftwareServer.objects.exclude(asset_id=self.asset_id).filter(hostname=self.cleaned_data.get('hostname')).count()
        if not n:
            return self.cleaned_data.get('hostname')
        else:
            raise ValidationError(_('主机名%(hostname)s已存在'), code='invalid', params={'hostname': hostname})


class AssetHandEditSoftwareServerForm(forms.Form):
    """编辑资产软件服务器手工录入视图表单验证类"""
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('softwareserver', '软件服务器')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    hostname = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='主机名',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    os_version = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='系统版本',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cpu_model = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='CPU型号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cpu_physical_count = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='CPU物理个数',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cpu_count = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='CPU逻辑个数',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    ram_total_capacity = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='内存总大小(MB)',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    disk_total_capacity = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='磁盘总大小(GB)',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    nic_name = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='网卡名称',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    nic_macaddress = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='MAC',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    nic_ipaddress = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='IP',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetHandEditSoftwareServerForm, self).__init__(*args, **kwargs)
        self.asset_id = self.initial['asset_id']
        self.fields['asset_type'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_type')
        for item in list(query_set):
            self.fields['asset_type'].initial.append(item['asset_type'])
        self.fields['business_unit_id'].widget.choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        self.fields['business_unit_id'].widget.choices.insert(0, (None, ''))
        self.fields['business_unit_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('business_unit_id')
        for item in list(query_set):
            self.fields['business_unit_id'].initial.append(item['business_unit_id'])
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        self.fields['tag_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('tag__id')
        for item in list(query_set):
            self.fields['tag_id'].initial.append(item['tag__id'])
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices
        self.fields['idc_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('idc_id')
        for item in list(query_set):
            self.fields['idc_id'].initial.append(item['idc_id'])
        self.fields['asset_status'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_status')
        for item in list(query_set):
            self.fields['asset_status'].initial.append(item['asset_status'])
        self.fields['hostname'].initial = models.SoftwareServer.objects.filter(asset_id=self.asset_id).first().hostname
        self.fields['os_version'].initial = models.SoftwareServer.objects.filter(asset_id=self.asset_id).first().os_version
        self.fields['memo'].initial = models.Asset.objects.filter(id=self.asset_id).first().memo
        self.fields['cpu_model'].initial = models.CPU.objects.filter(asset_id=self.asset_id).first().cpu_model
        self.fields['cpu_physical_count'].initial = models.CPU.objects.filter(asset_id=self.asset_id).first().cpu_physical_count
        self.fields['cpu_count'].initial = models.CPU.objects.filter(asset_id=self.asset_id).first().cpu_count
        self.fields['ram_total_capacity'].initial = models.RAM.objects.filter(asset_id=self.asset_id).first().total_capacity
        self.fields['disk_total_capacity'].initial = models.Disk.objects.filter(asset_id=self.asset_id).first().total_capacity
        self.fields['nic_name'].initial = models.NIC.objects.filter(asset_id=self.asset_id).first().name
        self.fields['nic_macaddress'].initial = models.NIC.objects.filter(asset_id=self.asset_id).first().macaddress
        self.fields['nic_ipaddress'].initial = models.NIC.objects.filter(asset_id=self.asset_id).first().ipaddress

    def clean_hostname(self):
        hostname = self.cleaned_data.get('hostname')
        n = models.SoftwareServer.objects.exclude(asset_id=self.asset_id).filter(hostname=hostname).count()
        if not n:
            return self.cleaned_data.get('hostname')
        else:
            raise ValidationError(_('主机名%(hostname)s已存在'), code='invalid', params={'hostname': hostname})

    def clean_nic_macaddress(self):
        macaddress = self.cleaned_data.get('nic_macaddress')
        n = models.NIC.objects.exclude(asset_id=self.asset_id).filter(macaddress=macaddress).count()
        if not n:
            return self.cleaned_data.get('nic_macaddress')
        else:
            raise ValidationError(_('MAC%(macaddress)s已存在'), code='invalid', params={'macaddress': macaddress})


class AssetEditNetworkDeviceForm(forms.Form):
    """编辑网络设备视图表单验证类"""
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('networkdevice', '网络设备')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    cabinet_num = fields.CharField(
        required=False,
        max_length=32,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于32位'},
        label='机柜号',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_begin_order = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='机柜起始序号(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_occupy_num = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='设备大小(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    device_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='设备类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('switch', '交换机'), ('firewall', '防火墙')],
            attrs={'class': 'form-control'}
        )
    )
    manufacturer = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='厂商',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('h3c', '华三'), ('juniper', '瞻博')],
            attrs={'class': 'form-control'}
        )
    )
    sn = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='SN号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    manager_ip = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='管理IP',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    purchasing_company = fields.CharField(
        required=False,
        max_length=64,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='采购公司',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    trade_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='购买时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    expire_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='保修到期时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetEditNetworkDeviceForm, self).__init__(*args, **kwargs)
        self.asset_id = self.initial['asset_id']
        self.fields['asset_type'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_type')
        for item in list(query_set):
            self.fields['asset_type'].initial.append(item['asset_type'])
        self.fields['business_unit_id'].widget.choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        self.fields['business_unit_id'].widget.choices.insert(0, (None, ''))
        self.fields['business_unit_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('business_unit_id')
        for item in list(query_set):
            self.fields['business_unit_id'].initial.append(item['business_unit_id'])
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        self.fields['tag_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('tag__id')
        for item in list(query_set):
            self.fields['tag_id'].initial.append(item['tag__id'])
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices
        self.fields['idc_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('idc_id')
        for item in list(query_set):
            self.fields['idc_id'].initial.append(item['idc_id'])
        self.fields['cabinet_num'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_num
        self.fields['cabinet_begin_order'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_begin_order
        self.fields['cabinet_occupy_num'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_occupy_num
        self.fields['purchasing_company'].initial = models.Asset.objects.filter(id=self.asset_id).first().purchasing_company
        self.fields['trade_date'].initial = models.Asset.objects.filter(id=self.asset_id).first().trade_date
        self.fields['expire_date'].initial = models.Asset.objects.filter(id=self.asset_id).first().expire_date
        self.fields['asset_status'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_status')
        for item in list(query_set):
            self.fields['asset_status'].initial.append(item['asset_status'])
        self.fields['device_type'].initial = []
        query_set = models.NetworkDevice.objects.filter(asset_id=self.asset_id).values('device_type')
        for item in list(query_set):
            self.fields['device_type'].initial.append(item['device_type'])
        self.fields['manufacturer'].initial = []
        query_set = models.NetworkDevice.objects.filter(asset_id=self.asset_id).values('manufacturer')
        for item in list(query_set):
            self.fields['manufacturer'].initial.append(item['manufacturer'])
        self.fields['sn'].initial = models.NetworkDevice.objects.filter(asset_id=self.asset_id).first().sn
        self.fields['manager_ip'].initial = models.NetworkDevice.objects.filter(
            asset_id=self.asset_id).first().manager_ip
        self.fields['memo'].initial = models.Asset.objects.filter(id=self.asset_id).first().memo

    def clean_sn(self):
        sn = self.cleaned_data.get('sn')
        n = models.NetworkDevice.objects.exclude(asset_id=self.asset_id).filter(sn=self.cleaned_data.get('sn')).count()
        if not n:
            return self.cleaned_data.get('sn')
        else:
            raise ValidationError(_('SN号%(sn)s已存在'), code='invalid', params={'sn': sn})

    def clean_manager_ip(self):
        manager_ip = self.cleaned_data.get('manager_ip')
        n = models.NetworkDevice.objects.exclude(asset_id=self.asset_id).filter(
            manager_ip=self.cleaned_data.get('manager_ip')).count()
        if not n:
            return self.cleaned_data.get('manager_ip')
        else:
            raise ValidationError(_('管理IP%(manager_ip)s已存在'), code='invalid', params={'manager_ip': manager_ip})


class AssetHandEditSecurityDeviceForm(forms.Form):
    """编辑安全设备视图表单验证类"""
    asset_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('securitydevice', '安全设备')],
            attrs={'class': 'form-control'}
        )
    )
    asset_status = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='资产状态',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('online', '在线'), ('offline', '离线'), ('putaway', '上架'), ('removeoff', '下架')],
            attrs={'class': 'form-control'}
        )
    )
    business_unit_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='所属业务线',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    idc_id = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='IDC机房',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )
    cabinet_num = fields.CharField(
        required=False,
        max_length=32,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于32位'},
        label='机柜号',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_begin_order = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='机柜起始序号(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    cabinet_occupy_num = fields.IntegerField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='设备大小(U)',
        widget=widgets.NumberInput(
            attrs={'class': 'form-control'}
        )
    )
    device_name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='设备名称',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    device_type = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='设备类型',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('waf', 'WAF'), ('ads', 'ADS'), ('ips', 'IPS')],
            attrs={'class': 'form-control'}
        )
    )
    manufacturer = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='厂商',
        help_text='必填项',
        widget=widgets.Select(
            choices=[('nsfocus', '绿盟')],
            attrs={'class': 'form-control'}
        )
    )
    sn = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='SN号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    manager_ip = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='管理IP',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    model = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='型号',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    port_number = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='接口数',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    purchasing_company = fields.CharField(
        required=False,
        max_length=64,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='采购公司',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    trade_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='购买时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    expire_date = fields.DateField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='保修到期时间',
        input_formats=['%Y-%m-%d'],
        widget=widgets.DateInput(
            attrs={'class': 'form-control form_datetime',
                   'data-date-format': 'yyyy-mm-dd'}
        )
    )
    tag_id = fields.MultipleChoiceField(
        required=False,
        error_messages={'invalid': '格式错误'},
        label='标签',
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={'class': 'form-control',
                   'size': 5}
        )
    )
    memo = fields.CharField(
        required=False,
        max_length=128,
        error_messages={'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='备注',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(AssetHandEditSecurityDeviceForm, self).__init__(*args, **kwargs)
        self.asset_id = self.initial['asset_id']
        self.fields['asset_type'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_type')
        for item in list(query_set):
            self.fields['asset_type'].initial.append(item['asset_type'])
        self.fields['business_unit_id'].widget.choices = list(models.BusinessUnit.objects.values_list('id', 'name'))
        self.fields['business_unit_id'].widget.choices.insert(0, (None, ''))
        self.fields['business_unit_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('business_unit_id')
        for item in list(query_set):
            self.fields['business_unit_id'].initial.append(item['business_unit_id'])
        self.fields['tag_id'].choices = models.Tag.objects.values_list('id', 'name')
        self.fields['tag_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('tag__id')
        for item in list(query_set):
            self.fields['tag_id'].initial.append(item['tag__id'])
        temp = list(models.IDC.objects.values_list('id', 'name', 'floor'))
        idc_id_choices = [(None, '')]
        for item in temp:
            idc_id_choices.append((item[0], '%s-%s' % (item[1], item[2])))
        self.fields['idc_id'].widget.choices = idc_id_choices
        self.fields['idc_id'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('idc_id')
        for item in list(query_set):
            self.fields['idc_id'].initial.append(item['idc_id'])
        self.fields['cabinet_num'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_num
        self.fields['cabinet_begin_order'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_begin_order
        self.fields['cabinet_occupy_num'].initial = models.Asset.objects.filter(id=self.asset_id).first().cabinet_occupy_num
        self.fields['trade_date'].initial = models.Asset.objects.filter(id=self.asset_id).first().trade_date
        self.fields['expire_date'].initial = models.Asset.objects.filter(id=self.asset_id).first().expire_date
        self.fields['purchasing_company'].initial = models.Asset.objects.filter(
            id=self.asset_id).first().purchasing_company
        self.fields['asset_status'].initial = []
        query_set = models.Asset.objects.filter(id=self.asset_id).values('asset_status')
        for item in list(query_set):
            self.fields['asset_status'].initial.append(item['asset_status'])
        self.fields['device_type'].initial = []
        query_set = models.SecurityDevice.objects.filter(asset_id=self.asset_id).values('device_type')
        for item in list(query_set):
            self.fields['device_type'].initial.append(item['device_type'])
        self.fields['manufacturer'].initial = []
        query_set = models.SecurityDevice.objects.filter(asset_id=self.asset_id).values('manufacturer')
        for item in list(query_set):
            self.fields['manufacturer'].initial.append(item['manufacturer'])
        self.fields['sn'].initial = models.SecurityDevice.objects.filter(asset_id=self.asset_id).first().sn
        self.fields['manager_ip'].initial = models.SecurityDevice.objects.filter(
            asset_id=self.asset_id).first().manager_ip
        self.fields['model'].initial = models.SecurityDevice.objects.filter(asset_id=self.asset_id).first().model
        self.fields['port_number'].initial = models.SecurityDevice.objects.filter(asset_id=self.asset_id).first().port_number
        self.fields['device_name'].initial = models.SecurityDevice.objects.filter(asset_id=self.asset_id).first().device_name
        self.fields['memo'].initial = models.Asset.objects.filter(id=self.asset_id).first().memo

    def clean_sn(self):
        sn = self.cleaned_data.get('sn')
        n = models.SecurityDevice.objects.exclude(asset_id=self.asset_id).filter(sn=self.cleaned_data.get('sn')).count()
        if not n:
            return self.cleaned_data.get('sn')
        else:
            raise ValidationError(_('SN号%(sn)s已存在'), code='invalid', params={'sn': sn})

    def clean_manager_ip(self):
        manager_ip = self.cleaned_data.get('manager_ip')
        n = models.SecurityDevice.objects.exclude(asset_id=self.asset_id).filter(
            manager_ip=self.cleaned_data.get('manager_ip')).count()
        if not n:
            return self.cleaned_data.get('manager_ip')
        else:
            raise ValidationError(_('管理IP%(manager_ip)s已存在'), code='invalid', params={'manager_ip': manager_ip})
