import xlwt
import os
import sys
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from cmdb_web.service import asset
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from cmdb_web.forms import asset_form
from cmdb_data import models
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from utils.permissions import check_permission
from utils.response import BaseResponse


@login_required
@check_permission
def asset_page(request):
    """
    资产视图
    :param request:
    :return:
    """
    return render(request, 'asset.html')


@login_required
def asset_json(request):
    """
    获取资产数据视图
    :param request:
    :return:
    """
    obj = asset.Asset()
    response = obj.fetch_asset(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def update_asset_json(request):
    """
    更新资产数据视图
    :param request:
    :return:
    """
    response = asset.Asset.update_asset(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def delete_asset_json(request):
    """
    删除资产数据视图
    :param request:
    :return:
    """
    response = asset.Asset.delete_asset(request)
    return JsonResponse(response.__dict__)


@login_required
@check_permission
def asset_detail(request, *args, **kwargs):
    """
    资产详情视图
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    asset_id = kwargs['asset_id']
    asset_type = kwargs['asset_type']
    response = asset.Asset.asset_detail(asset_id)
    return render(request, 'asset_detail.html', {'response': response,
                                                 'asset_type': asset_type,
                                                 'asset_id': asset_id})


@login_required
@check_permission
def asset_add(request):
    """
    添加资产视图
    :param request:
    :return:
    """
    return render(request, 'asset_add.html')


@login_required
@check_permission
def asset_add_hardware_server(request):
    """
    添加硬件服务器资产视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        form_obj = asset_form.AssetAddHardwareServerForm(request.POST)
        if form_obj.is_valid():
            tag_id_list = form_obj.cleaned_data.pop('tag_id')
            server_dict = {}
            server_dict['sn'] = form_obj.cleaned_data.pop('sn')
            server_dict['manager_ip'] = form_obj.cleaned_data.pop('manager_ip')
            server_dict['manufacturer'] = form_obj.cleaned_data.pop('manufacturer')
            try:
                with transaction.atomic():
                    asset_obj = models.Asset.objects.create(**form_obj.cleaned_data)
                    asset_obj.tag.add(*tag_id_list)
                    server_dict['asset'] = asset_obj
                    models.HardwareServer.objects.create(**server_dict)
                return redirect('/cmdb_web/asset.html')
            except Exception as e:
                raise ValidationError(_('添加资产失败'), code='invalid')
        else:
            return render(request, 'asset_add_hardware_server.html', {'form_obj': form_obj})
    elif request.method == 'GET':
        form_obj = asset_form.AssetAddHardwareServerForm()
        return render(request, 'asset_add_hardware_server.html', {'form_obj': form_obj})


@login_required
@check_permission
def asset_add_software_server(request):
    """
    添加软件服务器资产视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        form_obj = asset_form.AssetAddSoftwareServerForm(request.POST)
        if form_obj.is_valid():
            tag_id_list = form_obj.cleaned_data.pop('tag_id')
            server_dict = {}
            server_dict['hostname'] = form_obj.cleaned_data.pop('hostname')
            try:
                with transaction.atomic():
                    asset_obj = models.Asset.objects.create(**form_obj.cleaned_data)
                    asset_obj.tag.add(*tag_id_list)
                    server_dict['asset'] = asset_obj
                    models.SoftwareServer.objects.create(**server_dict)
                return redirect('/cmdb_web/asset.html')
            except Exception as e:
                raise ValidationError(_('添加资产失败'), code='invalid')
        else:
            return render(request, 'asset_add_software_server.html', {'form_obj': form_obj})
    elif request.method == 'GET':
        form_obj = asset_form.AssetAddSoftwareServerForm()
        return render(request, 'asset_add_software_server.html', {'form_obj': form_obj})


@login_required
@check_permission
def asset_hand_add_software_server(request):
    """
    添加手工录入软件服务器资产视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        form_obj = asset_form.AssetHandAddSoftwareServerForm(request.POST)
        if form_obj.is_valid():
            tag_id_list = form_obj.cleaned_data.pop('tag_id')
            server_dict = {}
            server_dict['hostname'] = form_obj.cleaned_data.pop('hostname')
            server_dict['os_version'] = form_obj.cleaned_data.pop('os_version')
            cpu_dict = {}
            cpu_dict['cpu_model'] = form_obj.cleaned_data.pop('cpu_model')
            cpu_dict['cpu_physical_count'] = form_obj.cleaned_data.pop('cpu_physical_count')
            cpu_dict['cpu_count'] = form_obj.cleaned_data.pop('cpu_count')
            ram_total_capacity = form_obj.cleaned_data.pop('ram_total_capacity')
            disk_total_capacity = form_obj.cleaned_data.pop('disk_total_capacity')
            nic_dict = {}
            nic_dict['name'] = form_obj.cleaned_data.pop('nic_name')
            nic_dict['macaddress'] = form_obj.cleaned_data.pop('nic_macaddress')
            nic_dict['ipaddress'] = form_obj.cleaned_data.pop('nic_ipaddress')
            try:
                with transaction.atomic():
                    asset_obj = models.Asset.objects.create(**form_obj.cleaned_data)
                    asset_obj.auto = False
                    asset_obj.save()
                    asset_obj.tag.add(*tag_id_list)
                    server_dict['asset'] = asset_obj
                    models.SoftwareServer.objects.create(**server_dict)
                    cpu_dict['asset'] = asset_obj
                    models.CPU.objects.create(**cpu_dict)
                    models.RAM.objects.create(asset=asset_obj, total_capacity=ram_total_capacity)
                    models.Disk.objects.create(asset=asset_obj, total_capacity=disk_total_capacity)
                    nic_dict['asset'] = asset_obj
                    models.NIC.objects.create(**nic_dict)
                return redirect('/cmdb_web/asset.html')
            except Exception as e:
                raise ValidationError(_('添加资产失败'), code='invalid')
        else:
            return render(request, 'asset_hand_add_software_server.html', {'form_obj': form_obj})
    elif request.method == 'GET':
        form_obj = asset_form.AssetHandAddSoftwareServerForm()
        return render(request, 'asset_hand_add_software_server.html', {'form_obj': form_obj})


@login_required
@check_permission
def asset_add_network_device(request):
    """添加网络设备资产视图"""
    if request.method == 'POST':
        form_obj = asset_form.AssetAddNetworkDeviceForm(request.POST)
        if form_obj.is_valid():
            tag_id_list = form_obj.cleaned_data.pop('tag_id')
            device_dict = {}
            device_dict['device_type'] = form_obj.cleaned_data.pop('device_type')
            device_dict['sn'] = form_obj.cleaned_data.pop('sn')
            device_dict['manager_ip'] = form_obj.cleaned_data.pop('manager_ip')
            device_dict['manufacturer'] = form_obj.cleaned_data.pop('manufacturer')
            try:
                with transaction.atomic():
                    asset_obj = models.Asset.objects.create(**form_obj.cleaned_data)
                    asset_obj.tag.add(*tag_id_list)
                    device_dict['asset'] = asset_obj
                    models.NetworkDevice.objects.create(**device_dict)
                return redirect('/cmdb_web/asset.html')
            except Exception as e:
                raise ValidationError(_('添加资产失败'), code='invalid')
        else:
            return render(request, 'asset_add_network_device.html', {'form_obj': form_obj})
    elif request.method == 'GET':
        form_obj = asset_form.AssetAddNetworkDeviceForm()
        return render(request, 'asset_add_network_device.html', {'form_obj': form_obj})


@login_required
@check_permission
def asset_hand_add_security_device(request):
    """添加安全设备资产视图"""
    if request.method == 'POST':
        form_obj = asset_form.AssetHandAddSecurityDeviceForm(request.POST)
        if form_obj.is_valid():
            tag_id_list = form_obj.cleaned_data.pop('tag_id')
            device_dict = {}
            device_dict['sn'] = form_obj.cleaned_data.pop('sn')
            device_dict['manager_ip'] = form_obj.cleaned_data.pop('manager_ip')
            device_dict['device_name'] = form_obj.cleaned_data.pop('device_name')
            device_dict['device_type'] = form_obj.cleaned_data.pop('device_type')
            device_dict['manufacturer'] = form_obj.cleaned_data.pop('manufacturer')
            device_dict['model'] = form_obj.cleaned_data.pop('model')
            device_dict['port_number'] = form_obj.cleaned_data.pop('port_number')
            try:
                with transaction.atomic():
                    asset_obj = models.Asset.objects.create(**form_obj.cleaned_data)
                    asset_obj.auto = False
                    asset_obj.save()
                    asset_obj.tag.add(*tag_id_list)
                    device_dict['asset'] = asset_obj
                    models.SecurityDevice.objects.create(**device_dict)
                return redirect('/cmdb_web/asset.html')
            except Exception as e:
                raise ValidationError(_('添加资产失败'), code='invalid')
        else:
            return render(request, 'asset_hand_add_security_device.html', {'form_obj': form_obj})
    elif request.method == 'GET':
        form_obj = asset_form.AssetHandAddSecurityDeviceForm()
        return render(request, 'asset_hand_add_security_device.html', {'form_obj': form_obj})


@login_required
@check_permission
def asset_edit(request, *args, **kwargs):
    """
    编辑资产视图
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    asset_type = kwargs['asset_type']
    asset_id = kwargs['asset_id']
    asset_auto = models.Asset.objects.filter(id=asset_id).first().auto
    if request.method == 'POST':
        if asset_type == 'hardwareserver':
            form_obj = asset_form.AssetEditHardwareServerForm(data=request.POST, initial={'asset_id': asset_id})
            if form_obj.is_valid():
                tag_id_list = form_obj.cleaned_data.pop('tag_id')
                server_dict = {}
                server_dict['manufacturer'] = form_obj.cleaned_data.pop('manufacturer')
                server_dict['sn'] = form_obj.cleaned_data.pop('sn')
                server_dict['manager_ip'] = form_obj.cleaned_data.pop('manager_ip')
                try:
                    with transaction.atomic():
                        asset_obj = models.Asset.objects.get(id=asset_id)
                        log_list = []
                        new_asset_type_id = form_obj.cleaned_data.get('asset_type')
                        for item in asset_obj.asset_type_choices:
                            if item[0] == new_asset_type_id:
                                new_asset_type = item[1]
                                break
                        old_asset_type_id = asset_obj.asset_type
                        for item in asset_obj.asset_type_choices:
                            if item[0] == old_asset_type_id:
                                old_asset_type = item[1]
                                break
                        if old_asset_type != new_asset_type:
                            log_list.append('[更新资产类型]:由%s变更为%s' % (old_asset_type, new_asset_type))
                        new_business_unit_id = form_obj.cleaned_data.get('business_unit_id')
                        if new_business_unit_id:
                            new_business_unit = models.BusinessUnit.objects.get(id=new_business_unit_id).name
                        else:
                            new_business_unit = None
                        if asset_obj.business_unit:
                            old_business_unit = asset_obj.business_unit.name
                        else:
                            old_business_unit = None
                        if old_business_unit != new_business_unit:
                            log_list.append('[更新业务线]:由%s变更为%s' % (old_business_unit, new_business_unit))
                        new_idc_id = form_obj.cleaned_data.get('idc_id')
                        if new_idc_id:
                            new_idc = models.IDC.objects.get(id=new_idc_id).name
                        else:
                            new_idc = None
                        if asset_obj.idc:
                            old_idc = asset_obj.idc.name
                        else:
                            old_idc = None
                        if old_idc != new_idc:
                            log_list.append('[更新IDC]:由%s变更为%s' % (old_idc, new_idc))
                        new_asset_status_id = form_obj.cleaned_data.get('asset_status')
                        for item in asset_obj.asset_status_choices:
                            if item[0] == new_asset_status_id:
                                new_asset_status = item[1]
                                break
                        old_asset_status_id = asset_obj.asset_status
                        for item in asset_obj.asset_status_choices:
                            if item[0] == old_asset_status_id:
                                old_asset_status = item[1]
                                break
                        if old_asset_status != new_asset_status:
                            log_list.append('[更新资产状态]:由%s变更为%s' % (old_asset_status, new_asset_status))
                        new_cabinet_num = form_obj.cleaned_data.get('cabinet_num')
                        if not new_cabinet_num:
                            new_cabinet_num = None
                        if asset_obj.cabinet_num:
                            old_cabinet_num = asset_obj.cabinet_num
                        else:
                            old_cabinet_num = None
                        if old_cabinet_num != new_cabinet_num:
                            log_list.append('[更新机柜号]:由%s变更为%s' % (old_cabinet_num, new_cabinet_num))
                        new_cabinet_begin_order = form_obj.cleaned_data.get('cabinet_begin_order')
                        if not new_cabinet_begin_order:
                            new_cabinet_begin_order = None
                        if asset_obj.cabinet_begin_order:
                            old_cabinet_begin_order = asset_obj.cabinet_begin_order
                        else:
                            old_cabinet_begin_order = None
                        if old_cabinet_begin_order != new_cabinet_begin_order:
                            log_list.append('[机柜起始序号(U)]:由%s变更为%s' % (old_cabinet_begin_order, new_cabinet_begin_order))
                        new_cabinet_occupy_num = form_obj.cleaned_data.get('cabinet_occupy_num')
                        if not new_cabinet_occupy_num:
                            new_cabinet_occupy_num = None
                        if asset_obj.cabinet_occupy_num:
                            old_cabinet_occupy_num = asset_obj.cabinet_occupy_num
                        else:
                            old_cabinet_occupy_num = None
                        if old_cabinet_occupy_num != new_cabinet_occupy_num:
                            log_list.append('[设备大小(U)]:由%s变更为%s' % (old_cabinet_occupy_num, new_cabinet_occupy_num))
                        new_purchasing_company = form_obj.cleaned_data.get('purchasing_company')
                        if not new_purchasing_company:
                            new_purchasing_company = None
                        if asset_obj.purchasing_company:
                            old_purchasing_company = asset_obj.purchasing_company
                        else:
                            old_purchasing_company = None
                        if old_purchasing_company != new_purchasing_company:
                            log_list.append('[更新采购公司]:由%s变更为%s' % (old_purchasing_company, new_purchasing_company))
                        new_trade_date = form_obj.cleaned_data.get('trade_date')
                        if not new_trade_date:
                            new_trade_date = None
                        if asset_obj.trade_date:
                            old_trade_date = asset_obj.trade_date
                        else:
                            old_trade_date = None
                        if old_trade_date != new_trade_date:
                            log_list.append('[更新购买时间]:由%s变更为%s' % (old_trade_date, new_trade_date))
                        new_expire_date = form_obj.cleaned_data.get('expire_date')
                        if not new_expire_date:
                            new_expire_date = None
                        if asset_obj.expire_date:
                            old_expire_date = asset_obj.expire_date
                        else:
                            old_expire_date = None
                        if old_expire_date != new_expire_date:
                            log_list.append('[更新保修到期时间]:由%s变更为%s' % (old_expire_date, new_expire_date))
                        new_memo = form_obj.cleaned_data.get('memo')
                        if not new_memo:
                            new_memo = None
                        if asset_obj.memo:
                            old_memo = asset_obj.memo
                        else:
                            old_memo = None
                        if old_memo != new_memo:
                            log_list.append('[更新备注]:由%s变更为%s' % (old_memo, new_memo))
                        models.Asset.objects.filter(id=asset_id).update(**form_obj.cleaned_data)
                        asset_obj.tag.set(tag_id_list)
                        server_obj = models.HardwareServer.objects.get(asset_id=asset_id)
                        new_manufacturer_id = server_dict['manufacturer']
                        for item in server_obj.manufacturer_choices:
                            if item[0] == new_manufacturer_id:
                                new_manufacturer = item[1]
                        old_manufacturer_id = server_obj.manufacturer
                        for item in server_obj.manufacturer_choices:
                            if item[0] == old_manufacturer_id:
                                old_manufacturer = item[1]
                        if old_manufacturer != new_manufacturer:
                            log_list.append('[更新厂商]:由%s变更为%s' % (old_manufacturer, new_manufacturer))
                            server_obj.manufacturer = new_manufacturer_id
                        new_sn = server_dict['sn']
                        old_sn = server_obj.sn
                        if old_sn != new_sn:
                            log_list.append('[更新SN号]:由%s变更为%s' % (old_sn, new_sn))
                            server_obj.sn = new_sn
                        new_manager_ip = server_dict['manager_ip']
                        old_manager_ip = server_obj.manager_ip
                        if old_manager_ip != new_manager_ip:
                            log_list.append('[更新管理IP]:由%s变更为%s' % (old_manager_ip, new_manager_ip))
                            server_obj.manager_ip = new_manager_ip
                        server_obj.save()
                        user_obj = request.user
                        if log_list:
                            models.AssetRecord.objects.create(asset=asset_obj,
                                                              creator=user_obj,
                                                              content=';'.join(log_list))
                    return redirect('/cmdb_web/asset.html')
                except Exception as e:
                    raise ValidationError(_('更新资产失败'), code='invalid')
            else:
                return render(request, 'asset_edit.html', {'form_obj': form_obj,
                                                           'asset_id': asset_id,
                                                           'asset_type': asset_type})
        elif asset_type == 'softwareserver':
            if asset_auto:  # 自动获取
                form_obj = asset_form.AssetEditSoftwareServerForm(data=request.POST, initial={'asset_id': asset_id})
                if form_obj.is_valid():
                    tag_id_list = form_obj.cleaned_data.pop('tag_id')
                    server_dict = {}
                    server_dict['hostname'] = form_obj.cleaned_data.pop('hostname')
                    try:
                        with transaction.atomic():
                            asset_obj = models.Asset.objects.get(id=asset_id)
                            log_list = []
                            new_asset_type_id = form_obj.cleaned_data.get('asset_type')
                            for item in asset_obj.asset_type_choices:
                                if item[0] == new_asset_type_id:
                                    new_asset_type = item[1]
                                    break
                            old_asset_type_id = asset_obj.asset_type
                            for item in asset_obj.asset_type_choices:
                                if item[0] == old_asset_type_id:
                                    old_asset_type = item[1]
                                    break
                            if old_asset_type != new_asset_type:
                                log_list.append('[更新资产类型]:由%s变更为%s' % (old_asset_type, new_asset_type))
                            new_business_unit_id = form_obj.cleaned_data.get('business_unit_id')
                            if new_business_unit_id:
                                new_business_unit = models.BusinessUnit.objects.get(id=new_business_unit_id).name
                            else:
                                new_business_unit = None
                            if asset_obj.business_unit:
                                old_business_unit = asset_obj.business_unit.name
                            else:
                                old_business_unit = None
                            if old_business_unit != new_business_unit:
                                log_list.append('[更新业务线]:由%s变更为%s' % (old_business_unit, new_business_unit))
                            new_idc_id = form_obj.cleaned_data.get('idc_id')
                            if new_idc_id:
                                new_idc = models.IDC.objects.get(id=new_idc_id).name
                            else:
                                new_idc = None
                            if asset_obj.idc:
                                old_idc = asset_obj.idc.name
                            else:
                                old_idc = None
                            if old_idc != new_idc:
                                log_list.append('[更新IDC]:由%s变更为%s' % (old_idc, new_idc))
                            new_asset_status_id = form_obj.cleaned_data.get('asset_status')
                            for item in asset_obj.asset_status_choices:
                                if item[0] == new_asset_status_id:
                                    new_asset_status = item[1]
                                    break
                            old_asset_status_id = asset_obj.asset_status
                            for item in asset_obj.asset_status_choices:
                                if item[0] == old_asset_status_id:
                                    old_asset_status = item[1]
                                    break
                            if old_asset_status != new_asset_status:
                                log_list.append('[更新资产状态]:由%s变更为%s' % (old_asset_status, new_asset_status))
                            new_memo = form_obj.cleaned_data.get('memo')
                            if not new_memo:
                                new_memo = None
                            if asset_obj.memo:
                                old_memo = asset_obj.memo
                            else:
                                old_memo = None
                            if old_memo != new_memo:
                                log_list.append('[更新备注]:由%s变更为%s' % (old_memo, new_memo))
                            models.Asset.objects.filter(id=asset_id).update(**form_obj.cleaned_data)
                            asset_obj.tag.set(tag_id_list)
                            server_obj = models.SoftwareServer.objects.get(asset_id=asset_id)
                            new_hostname = server_dict['hostname']
                            old_hostname = server_obj.hostname
                            if old_hostname != new_hostname:
                                log_list.append('[更新主机名]:由%s变更为%s' % (old_hostname, new_hostname))
                                server_obj.hostname = new_hostname
                            server_obj.save()
                            user_obj = request.user
                            if log_list:
                                models.AssetRecord.objects.create(asset=asset_obj,
                                                                  creator=user_obj,
                                                                  content=';'.join(log_list))
                        return redirect('/cmdb_web/asset.html')
                    except Exception as e:
                        raise ValidationError(_('更新资产失败'), code='invalid')
                else:
                    return render(request, 'asset_edit.html', {'form_obj': form_obj,
                                                               'asset_id': asset_id,
                                                               'asset_type': asset_type})
            else:  # 手动获取
                form_obj = asset_form.AssetHandEditSoftwareServerForm(data=request.POST, initial={'asset_id': asset_id})
                if form_obj.is_valid():
                    tag_id_list = form_obj.cleaned_data.pop('tag_id')
                    server_dict = {}
                    server_dict['hostname'] = form_obj.cleaned_data.pop('hostname')
                    server_dict['os_version'] = form_obj.cleaned_data.pop('os_version')
                    cpu_dict = {}
                    cpu_dict['cpu_model'] = form_obj.cleaned_data.pop('cpu_model')
                    cpu_dict['cpu_physical_count'] = form_obj.cleaned_data.pop('cpu_physical_count')
                    cpu_dict['cpu_count'] = form_obj.cleaned_data.pop('cpu_count')
                    ram_total_capacity = form_obj.cleaned_data.pop('ram_total_capacity')
                    disk_total_capacity = form_obj.cleaned_data.pop('disk_total_capacity')
                    nic_dict = {}
                    nic_dict['nic_name'] = form_obj.cleaned_data.pop('nic_name')
                    nic_dict['nic_macaddress'] = form_obj.cleaned_data.pop('nic_macaddress')
                    nic_dict['nic_ipaddress'] = form_obj.cleaned_data.pop('nic_ipaddress')
                    try:
                        with transaction.atomic():
                            asset_obj = models.Asset.objects.get(id=asset_id)
                            log_list = []
                            new_asset_type_id = form_obj.cleaned_data.get('asset_type')
                            for item in asset_obj.asset_type_choices:
                                if item[0] == new_asset_type_id:
                                    new_asset_type = item[1]
                                    break
                            old_asset_type_id = asset_obj.asset_type
                            for item in asset_obj.asset_type_choices:
                                if item[0] == old_asset_type_id:
                                    old_asset_type = item[1]
                                    break
                            if old_asset_type != new_asset_type:
                                log_list.append('[更新资产类型]:由%s变更为%s' % (old_asset_type, new_asset_type))
                            new_business_unit_id = form_obj.cleaned_data.get('business_unit_id')
                            if new_business_unit_id:
                                new_business_unit = models.BusinessUnit.objects.get(id=new_business_unit_id).name
                            else:
                                new_business_unit = None
                            if asset_obj.business_unit:
                                old_business_unit = asset_obj.business_unit.name
                            else:
                                old_business_unit = None
                            if old_business_unit != new_business_unit:
                                log_list.append('[更新业务线]:由%s变更为%s' % (old_business_unit, new_business_unit))
                            new_idc_id = form_obj.cleaned_data.get('idc_id')
                            if new_idc_id:
                                new_idc = models.IDC.objects.get(id=new_idc_id).name
                            else:
                                new_idc = None
                            if asset_obj.idc:
                                old_idc = asset_obj.idc.name
                            else:
                                old_idc = None
                            if old_idc != new_idc:
                                log_list.append('[更新IDC]:由%s变更为%s' % (old_idc, new_idc))
                            new_asset_status_id = form_obj.cleaned_data.get('asset_status')
                            for item in asset_obj.asset_status_choices:
                                if item[0] == new_asset_status_id:
                                    new_asset_status = item[1]
                                    break
                            old_asset_status_id = asset_obj.asset_status
                            for item in asset_obj.asset_status_choices:
                                if item[0] == old_asset_status_id:
                                    old_asset_status = item[1]
                                    break
                            if old_asset_status != new_asset_status:
                                log_list.append('[更新资产状态]:由%s变更为%s' % (old_asset_status, new_asset_status))
                            new_memo = form_obj.cleaned_data.get('memo')
                            if not new_memo:
                                new_memo = None
                            if asset_obj.memo:
                                old_memo = asset_obj.memo
                            else:
                                old_memo = None
                            if old_memo != new_memo:
                                log_list.append('[更新备注]:由%s变更为%s' % (old_memo, new_memo))
                            models.Asset.objects.filter(id=asset_id).update(**form_obj.cleaned_data)
                            asset_obj.tag.set(tag_id_list)
                            server_obj = models.SoftwareServer.objects.get(asset_id=asset_id)
                            new_hostname = server_dict['hostname']
                            old_hostname = server_obj.hostname
                            if old_hostname != new_hostname:
                                log_list.append('[更新主机名]:由%s变更为%s' % (old_hostname, new_hostname))
                                server_obj.hostname = new_hostname
                            new_os_version = server_dict['os_version']
                            if not new_os_version:
                                new_os_version = None
                            old_os_version = server_obj.os_version
                            if not old_os_version:
                                old_os_version = None
                            if old_os_version != new_os_version:
                                log_list.append('[更新系统版本]:由%s变更为%s' % (old_os_version, new_os_version))
                                server_obj.os_version = new_os_version
                            server_obj.save()
                            cpu_obj = models.CPU.objects.filter(asset=asset_obj).first()
                            new_cpu_model = cpu_dict['cpu_model']
                            old_cpu_model = cpu_obj.cpu_model
                            if old_cpu_model != new_cpu_model:
                                log_list.append('[更新CPU型号]:由%s变更为%s' % (old_cpu_model, new_cpu_model))
                                cpu_obj.cpu_model = new_cpu_model
                            new_cpu_physical_count = cpu_dict['cpu_physical_count']
                            old_cpu_physical_count = cpu_obj.cpu_physical_count
                            if old_cpu_physical_count != new_cpu_physical_count:
                                log_list.append(
                                    '[更新CPU物理个数]:由%s变更为%s' % (old_cpu_physical_count, new_cpu_physical_count))
                                cpu_obj.cpu_physical_count = new_cpu_physical_count
                            new_cpu_count = cpu_dict['cpu_count']
                            old_cpu_count = cpu_obj.cpu_count
                            if old_cpu_count != new_cpu_count:
                                log_list.append('[更新CPU逻辑个数]:由%s变更为%s' % (old_cpu_count, new_cpu_count))
                                cpu_obj.cpu_count = new_cpu_count
                            cpu_obj.save()
                            ram_obj = models.RAM.objects.filter(asset=asset_obj).first()
                            new_ram_total_capacity = ram_total_capacity
                            old_ram_total_capacity = ram_obj.total_capacity
                            if old_ram_total_capacity != new_ram_total_capacity:
                                log_list.append('[更新内存总大小]:由%s变更为%s' % (old_ram_total_capacity, new_ram_total_capacity))
                                ram_obj.total_capacity = new_ram_total_capacity
                            ram_obj.save()
                            disk_obj = models.Disk.objects.filter(asset=asset_obj).first()
                            new_disk_total_capacity = disk_total_capacity
                            old_disk_total_capacity = disk_obj.total_capacity
                            if old_disk_total_capacity != new_disk_total_capacity:
                                log_list.append(
                                    '[更新硬盘总大小]:由%s变更为%s' % (old_disk_total_capacity, new_disk_total_capacity))
                                disk_obj.total_capacity = new_disk_total_capacity
                            disk_obj.save()
                            nic_obj = models.NIC.objects.filter(asset=asset_obj).first()
                            new_nic_name = nic_dict['nic_name']
                            old_nic_name = nic_obj.name
                            if old_nic_name != new_nic_name:
                                log_list.append('[更新网卡名称]:由%s变更为%s' % (old_nic_name, new_nic_name))
                                nic_obj.name = new_nic_name
                            new_nic_macaddress = nic_dict['nic_macaddress']
                            old_nic_macaddress = nic_obj.macaddress
                            if old_nic_macaddress != new_nic_macaddress:
                                log_list.append('[更新MAC]:由%s变更为%s' % (old_nic_macaddress, new_nic_macaddress))
                                nic_obj.macaddress = new_nic_macaddress
                            new_nic_ipaddress = nic_dict['nic_ipaddress']
                            old_nic_ipaddress = nic_obj.ipaddress
                            if old_nic_ipaddress != new_nic_ipaddress:
                                log_list.append('[更新IP]:由%s变更为%s' % (old_nic_ipaddress, new_nic_ipaddress))
                                nic_obj.ipaddress = new_nic_ipaddress
                            nic_obj.save()
                            user_obj = request.user
                            if log_list:
                                models.AssetRecord.objects.create(asset=asset_obj,
                                                                  creator=user_obj,
                                                                  content=';'.join(log_list))
                        return redirect('/cmdb_web/asset.html')
                    except Exception as e:
                        raise ValidationError(_('更新资产失败'), code='invalid')
                else:
                    return render(request, 'asset_edit.html', {'form_obj': form_obj,
                                                               'asset_id': asset_id,
                                                               'asset_type': asset_type})
        elif asset_type == 'networkdevice':
            form_obj = asset_form.AssetEditNetworkDeviceForm(data=request.POST, initial={'asset_id': asset_id})
            if form_obj.is_valid():
                tag_id_list = form_obj.cleaned_data.pop('tag_id')
                device_dict = {}
                device_dict['manufacturer'] = form_obj.cleaned_data.pop('manufacturer')
                device_dict['device_type'] = form_obj.cleaned_data.pop('device_type')
                device_dict['sn'] = form_obj.cleaned_data.pop('sn')
                device_dict['manager_ip'] = form_obj.cleaned_data.pop('manager_ip')
                try:
                    with transaction.atomic():
                        asset_obj = models.Asset.objects.get(id=asset_id)
                        log_list = []
                        new_asset_type_id = form_obj.cleaned_data.get('asset_type')
                        for item in asset_obj.asset_type_choices:
                            if item[0] == new_asset_type_id:
                                new_asset_type = item[1]
                                break
                        old_asset_type_id = asset_obj.asset_type
                        for item in asset_obj.asset_type_choices:
                            if item[0] == old_asset_type_id:
                                old_asset_type = item[1]
                                break
                        if old_asset_type != new_asset_type:
                            log_list.append('[更新资产类型]:由%s变更为%s' % (old_asset_type, new_asset_type))
                        new_business_unit_id = form_obj.cleaned_data.get('business_unit_id')
                        if new_business_unit_id:
                            new_business_unit = models.BusinessUnit.objects.get(id=new_business_unit_id).name
                        else:
                            new_business_unit = None
                        if asset_obj.business_unit:
                            old_business_unit = asset_obj.business_unit.name
                        else:
                            old_business_unit = None
                        if old_business_unit != new_business_unit:
                            log_list.append('[更新业务线]:由%s变更为%s' % (old_business_unit, new_business_unit))
                        new_idc_id = form_obj.cleaned_data.get('idc_id')
                        if new_idc_id:
                            new_idc = models.IDC.objects.get(id=new_idc_id).name
                        else:
                            new_idc = None
                        if asset_obj.idc:
                            old_idc = asset_obj.idc.name
                        else:
                            old_idc = None
                        if old_idc != new_idc:
                            log_list.append('[更新IDC]:由%s变更为%s' % (old_idc, new_idc))
                        new_asset_status_id = form_obj.cleaned_data.get('asset_status')
                        for item in asset_obj.asset_status_choices:
                            if item[0] == new_asset_status_id:
                                new_asset_status = item[1]
                                break
                        old_asset_status_id = asset_obj.asset_status
                        for item in asset_obj.asset_status_choices:
                            if item[0] == old_asset_status_id:
                                old_asset_status = item[1]
                                break
                        if old_asset_status != new_asset_status:
                            log_list.append('[更新资产状态]:由%s变更为%s' % (old_asset_status, new_asset_status))
                        new_cabinet_num = form_obj.cleaned_data.get('cabinet_num')
                        if not new_cabinet_num:
                            new_cabinet_num = None
                        if asset_obj.cabinet_num:
                            old_cabinet_num = asset_obj.cabinet_num
                        else:
                            old_cabinet_num = None
                        if old_cabinet_num != new_cabinet_num:
                            log_list.append('[更新机柜号]:由%s变更为%s' % (old_cabinet_num, new_cabinet_num))
                        new_cabinet_begin_order = form_obj.cleaned_data.get('cabinet_begin_order')
                        if not new_cabinet_begin_order:
                            new_cabinet_begin_order = None
                        if asset_obj.cabinet_begin_order:
                            old_cabinet_begin_order = asset_obj.cabinet_begin_order
                        else:
                            old_cabinet_begin_order = None
                        if old_cabinet_begin_order != new_cabinet_begin_order:
                            log_list.append('[机柜起始序号(U)]:由%s变更为%s' % (old_cabinet_begin_order, new_cabinet_begin_order))
                        new_cabinet_occupy_num = form_obj.cleaned_data.get('cabinet_occupy_num')
                        if not new_cabinet_occupy_num:
                            new_cabinet_occupy_num = None
                        if asset_obj.cabinet_occupy_num:
                            old_cabinet_occupy_num = asset_obj.cabinet_occupy_num
                        else:
                            old_cabinet_occupy_num = None
                        if old_cabinet_occupy_num != new_cabinet_occupy_num:
                            log_list.append('[设备大小(U)]:由%s变更为%s' % (old_cabinet_occupy_num, new_cabinet_occupy_num))
                        new_purchasing_company = form_obj.cleaned_data.get('purchasing_company')
                        if not new_purchasing_company:
                            new_purchasing_company = None
                        if asset_obj.purchasing_company:
                            old_purchasing_company = asset_obj.purchasing_company
                        else:
                            old_purchasing_company = None
                        if old_purchasing_company != new_purchasing_company:
                            log_list.append('[更新采购公司]:由%s变更为%s' % (old_purchasing_company, new_purchasing_company))
                        new_trade_date = form_obj.cleaned_data.get('trade_date')
                        if not new_trade_date:
                            new_trade_date = None
                        if asset_obj.trade_date:
                            old_trade_date = asset_obj.trade_date
                        else:
                            old_trade_date = None
                        if old_trade_date != new_trade_date:
                            log_list.append('[更新购买时间]:由%s变更为%s' % (old_trade_date, new_trade_date))
                        new_expire_date = form_obj.cleaned_data.get('expire_date')
                        if not new_expire_date:
                            new_expire_date = None
                        if asset_obj.expire_date:
                            old_expire_date = asset_obj.expire_date
                        else:
                            old_expire_date = None
                        if old_expire_date != new_expire_date:
                            log_list.append('[更新保修到期时间]:由%s变更为%s' % (old_expire_date, new_expire_date))
                        new_memo = form_obj.cleaned_data.get('memo')
                        if not new_memo:
                            new_memo = None
                        if asset_obj.memo:
                            old_memo = asset_obj.memo
                        else:
                            old_memo = None
                        if old_memo != new_memo:
                            log_list.append('[更新备注]:由%s变更为%s' % (old_memo, new_memo))
                        models.Asset.objects.filter(id=asset_id).update(**form_obj.cleaned_data)
                        asset_obj.tag.set(tag_id_list)
                        device_obj = models.NetworkDevice.objects.get(asset_id=asset_id)
                        new_device_type_id = device_dict['device_type']
                        for item in device_obj.device_type_choices:
                            if item[0] == new_device_type_id:
                                new_device_type = item[1]
                        old_device_type_id = device_obj.device_type
                        for item in device_obj.device_type_choices:
                            if item[0] == old_device_type_id:
                                old_device_type = item[1]
                        if old_device_type != new_device_type:
                            log_list.append('[更新设备类型]:由%s变更为%s' % (old_device_type, new_device_type))
                            device_obj.device_type = new_device_type_id
                        new_manufacturer_id = device_dict['manufacturer']
                        for item in device_obj.manufacturer_choices:
                            if item[0] == new_manufacturer_id:
                                new_manufacturer = item[1]
                        old_manufacturer_id = device_obj.manufacturer
                        for item in device_obj.manufacturer_choices:
                            if item[0] == old_manufacturer_id:
                                old_manufacturer = item[1]
                        if old_manufacturer != new_manufacturer:
                            log_list.append('[更新厂商]:由%s变更为%s' % (old_manufacturer, new_manufacturer))
                            device_obj.manufacturer = new_manufacturer_id
                        new_sn = device_dict['sn']
                        old_sn = device_obj.sn
                        if old_sn != new_sn:
                            log_list.append('[更新SN号]:由%s变更为%s' % (old_sn, new_sn))
                            device_obj.sn = new_sn
                        new_manager_ip = device_dict['manager_ip']
                        old_manager_ip = device_obj.manager_ip
                        if old_manager_ip != new_manager_ip:
                            log_list.append('[更新管理IP]:由%s变更为%s' % (old_manager_ip, new_manager_ip))
                            device_obj.manager_ip = new_manager_ip
                        device_obj.save()
                        user_obj = request.user
                        if log_list:
                            models.AssetRecord.objects.create(asset=asset_obj,
                                                              creator=user_obj,
                                                              content=';'.join(log_list))
                    return redirect('/cmdb_web/asset.html')
                except Exception as e:
                    raise ValidationError(_('更新资产失败'), code='invalid')
            else:
                return render(request, 'asset_edit.html', {'form_obj': form_obj,
                                                           'asset_id': asset_id,
                                                           'asset_type': asset_type})
        elif asset_type == 'securitydevice':
            form_obj = asset_form.AssetHandEditSecurityDeviceForm(data=request.POST, initial={'asset_id': asset_id})
            if form_obj.is_valid():
                tag_id_list = form_obj.cleaned_data.pop('tag_id')
                device_dict = {}
                device_dict['manufacturer'] = form_obj.cleaned_data.pop('manufacturer')
                device_dict['device_type'] = form_obj.cleaned_data.pop('device_type')
                device_dict['sn'] = form_obj.cleaned_data.pop('sn')
                device_dict['manager_ip'] = form_obj.cleaned_data.pop('manager_ip')
                device_dict['model'] = form_obj.cleaned_data.pop('model')
                device_dict['port_number'] = form_obj.cleaned_data.pop('port_number')
                device_dict['device_name'] = form_obj.cleaned_data.pop('device_name')
                device_dict['memo'] = form_obj.cleaned_data.pop('memo')
                try:
                    with transaction.atomic():
                        asset_obj = models.Asset.objects.get(id=asset_id)
                        log_list = []
                        new_asset_type_id = form_obj.cleaned_data.get('asset_type')
                        for item in asset_obj.asset_type_choices:
                            if item[0] == new_asset_type_id:
                                new_asset_type = item[1]
                                break
                        old_asset_type_id = asset_obj.asset_type
                        for item in asset_obj.asset_type_choices:
                            if item[0] == old_asset_type_id:
                                old_asset_type = item[1]
                                break
                        if old_asset_type != new_asset_type:
                            log_list.append('[更新资产类型]:由%s变更为%s' % (old_asset_type, new_asset_type))
                        new_business_unit_id = form_obj.cleaned_data.get('business_unit_id')
                        if new_business_unit_id:
                            new_business_unit = models.BusinessUnit.objects.get(id=new_business_unit_id).name
                        else:
                            new_business_unit = None
                        if asset_obj.business_unit:
                            old_business_unit = asset_obj.business_unit.name
                        else:
                            old_business_unit = None
                        if old_business_unit != new_business_unit:
                            log_list.append('[更新业务线]:由%s变更为%s' % (old_business_unit, new_business_unit))
                        new_idc_id = form_obj.cleaned_data.get('idc_id')
                        if new_idc_id:
                            new_idc = models.IDC.objects.get(id=new_idc_id).name
                        else:
                            new_idc = None
                        if asset_obj.idc:
                            old_idc = asset_obj.idc.name
                        else:
                            old_idc = None
                        if old_idc != new_idc:
                            log_list.append('[更新IDC]:由%s变更为%s' % (old_idc, new_idc))
                        new_asset_status_id = form_obj.cleaned_data.get('asset_status')
                        for item in asset_obj.asset_status_choices:
                            if item[0] == new_asset_status_id:
                                new_asset_status = item[1]
                                break
                        old_asset_status_id = asset_obj.asset_status
                        for item in asset_obj.asset_status_choices:
                            if item[0] == old_asset_status_id:
                                old_asset_status = item[1]
                                break
                        if old_asset_status != new_asset_status:
                            log_list.append('[更新资产状态]:由%s变更为%s' % (old_asset_status, new_asset_status))
                        new_cabinet_num = form_obj.cleaned_data.get('cabinet_num')
                        if not new_cabinet_num:
                            new_cabinet_num = None
                        if asset_obj.cabinet_num:
                            old_cabinet_num = asset_obj.cabinet_num
                        else:
                            old_cabinet_num = None
                        if old_cabinet_num != new_cabinet_num:
                            log_list.append('[更新机柜号]:由%s变更为%s' % (old_cabinet_num, new_cabinet_num))
                        new_cabinet_begin_order = form_obj.cleaned_data.get('cabinet_begin_order')
                        if not new_cabinet_begin_order:
                            new_cabinet_begin_order = None
                        if asset_obj.cabinet_begin_order:
                            old_cabinet_begin_order = asset_obj.cabinet_begin_order
                        else:
                            old_cabinet_begin_order = None
                        if old_cabinet_begin_order != new_cabinet_begin_order:
                            log_list.append('[机柜起始序号(U)]:由%s变更为%s' % (old_cabinet_begin_order, new_cabinet_begin_order))
                        new_cabinet_occupy_num = form_obj.cleaned_data.get('cabinet_occupy_num')
                        if not new_cabinet_occupy_num:
                            new_cabinet_occupy_num = None
                        if asset_obj.cabinet_occupy_num:
                            old_cabinet_occupy_num = asset_obj.cabinet_occupy_num
                        else:
                            old_cabinet_occupy_num = None
                        if old_cabinet_occupy_num != new_cabinet_occupy_num:
                            log_list.append('[设备大小(U)]:由%s变更为%s' % (old_cabinet_occupy_num, new_cabinet_occupy_num))
                        new_purchasing_company = form_obj.cleaned_data.get('purchasing_company')
                        if not new_purchasing_company:
                            new_purchasing_company = None
                        if asset_obj.purchasing_company:
                            old_purchasing_company = asset_obj.purchasing_company
                        else:
                            old_purchasing_company = None
                        if old_purchasing_company != new_purchasing_company:
                            log_list.append('[更新采购公司]:由%s变更为%s' % (old_purchasing_company, new_purchasing_company))
                        new_trade_date = form_obj.cleaned_data.get('trade_date')
                        if not new_trade_date:
                            new_trade_date = None
                        if asset_obj.trade_date:
                            old_trade_date = asset_obj.trade_date
                        else:
                            old_trade_date = None
                        if old_trade_date != new_trade_date:
                            log_list.append('[更新购买时间]:由%s变更为%s' % (old_trade_date, new_trade_date))
                        new_expire_date = form_obj.cleaned_data.get('expire_date')
                        if not new_expire_date:
                            new_expire_date = None
                        if asset_obj.expire_date:
                            old_expire_date = asset_obj.expire_date
                        else:
                            old_expire_date = None
                        if old_expire_date != new_expire_date:
                            log_list.append('[更新保修到期时间]:由%s变更为%s' % (old_expire_date, new_expire_date))
                        new_memo = form_obj.cleaned_data.get('memo')
                        if not new_memo:
                            new_memo = None
                        if asset_obj.memo:
                            old_memo = asset_obj.memo
                        else:
                            old_memo = None
                        if old_memo != new_memo:
                            log_list.append('[更新备注]:由%s变更为%s' % (old_memo, new_memo))
                        models.Asset.objects.filter(id=asset_id).update(**form_obj.cleaned_data)
                        asset_obj.tag.set(tag_id_list)
                        device_obj = models.SecurityDevice.objects.get(asset_id=asset_id)
                        new_device_type_id = device_dict['device_type']
                        for item in device_obj.device_type_choices:
                            if item[0] == new_device_type_id:
                                new_device_type = item[1]
                        old_device_type_id = device_obj.device_type
                        for item in device_obj.device_type_choices:
                            if item[0] == old_device_type_id:
                                old_device_type = item[1]
                        if old_device_type != new_device_type:
                            log_list.append('[更新设备类型]:由%s变更为%s' % (old_device_type, new_device_type))
                            device_obj.device_type = new_device_type_id
                        new_manufacturer_id = device_dict['manufacturer']
                        for item in device_obj.manufacturer_choices:
                            if item[0] == new_manufacturer_id:
                                new_manufacturer = item[1]
                        old_manufacturer_id = device_obj.manufacturer
                        for item in device_obj.manufacturer_choices:
                            if item[0] == old_manufacturer_id:
                                old_manufacturer = item[1]
                        if old_manufacturer != new_manufacturer:
                            log_list.append('[更新厂商]:由%s变更为%s' % (old_manufacturer, new_manufacturer))
                            device_obj.manufacturer = new_manufacturer_id
                        new_sn = device_dict['sn']
                        old_sn = device_obj.sn
                        if old_sn != new_sn:
                            log_list.append('[更新SN号]:由%s变更为%s' % (old_sn, new_sn))
                            device_obj.sn = new_sn
                        new_manager_ip = device_dict['manager_ip']
                        old_manager_ip = device_obj.manager_ip
                        if old_manager_ip != new_manager_ip:
                            log_list.append('[更新管理IP]:由%s变更为%s' % (old_manager_ip, new_manager_ip))
                            device_obj.manager_ip = new_manager_ip
                        new_device_name = device_dict['device_name']
                        old_device_name = device_obj.device_name
                        if old_device_name != new_device_name:
                            log_list.append('[更新设备名称]:由%s变更为%s' % (old_device_name, new_device_name))
                            device_obj.device_name = new_device_name
                        new_model = device_dict['model']
                        old_model = device_obj.model
                        if old_model != new_model:
                            log_list.append('[更新型号]:由%s变更为%s' % (old_model, new_model))
                            device_obj.model = new_model
                        new_port_number = device_dict['port_number']
                        old_port_number = device_obj.port_number
                        if old_port_number != new_port_number:
                            log_list.append('[更新接口数]:由%s变更为%s' % (old_port_number, new_port_number))
                            device_obj.port_number = new_port_number
                        device_obj.save()
                        user_obj = request.user
                        if log_list:
                            models.AssetRecord.objects.create(asset=asset_obj,
                                                              creator=user_obj,
                                                              content=';'.join(log_list))
                    return redirect('/cmdb_web/asset.html')
                except Exception as e:
                    raise ValidationError(_('更新资产失败'), code='invalid')
            else:
                return render(request, 'asset_edit.html', {'form_obj': form_obj,
                                                           'asset_id': asset_id,
                                                           'asset_type': asset_type})
    elif request.method == 'GET':
        if asset_type == 'hardwareserver':
            form_obj = asset_form.AssetEditHardwareServerForm(initial={'asset_id': asset_id})
        elif asset_type == 'softwareserver':
            if asset_auto:
                form_obj = asset_form.AssetEditSoftwareServerForm(initial={'asset_id': asset_id})
            else:
                form_obj = asset_form.AssetHandEditSoftwareServerForm(initial={'asset_id': asset_id})
        elif asset_type == 'networkdevice':
            form_obj = asset_form.AssetEditNetworkDeviceForm(initial={'asset_id': asset_id})
        elif asset_type == 'securitydevice':
            form_obj = asset_form.AssetHandEditSecurityDeviceForm(initial={'asset_id': asset_id})
        return render(request, 'asset_edit.html', {'form_obj': form_obj,
                                                   'asset_id': asset_id,
                                                   'asset_type': asset_type})


@login_required
@check_permission
def asset_detail_update_speed(request):
    response = BaseResponse()
    if request.method == 'POST':
        try:
            log_list = []
            nid = request.POST.get('nid')
            new_speed = request.POST.get('new_speed')
            disk_obj = models.Disk.objects.filter(id=nid).first()
            if disk_obj.speed != new_speed:
                log_list.append('[更新硬盘转速]:由%s变更为%s' % (disk_obj.speed, new_speed))
                disk_obj.speed = new_speed
                disk_obj.save()
                if log_list:
                    user_obj = request.user
                    models.AssetRecord.objects.create(asset_id=disk_obj.asset_id,
                                                      creator=user_obj,
                                                      content=';'.join(log_list))
        except Exception as e:
            response.status = False
            response.message = str(e)
        return JsonResponse(response.__dict__)


@csrf_exempt
@login_required
@check_permission
def asset_export(request):
    """资产导出视图"""
    if request.method == 'POST':
        response = BaseResponse()
        data = dict(request.POST)
        obj_list = models.Asset.objects.all()
        download_dir = settings.DOWNLOAD_DIR
        for key, value_list in data.items():
            q = Q()
            q.connector = 'OR'
            for value in value_list:
                if value:
                    q.children.append((key, value))
            obj_list = obj_list.filter(q).all()

        hardware_server_title = ['资产ID', '业务线', 'IDC', '机柜号', '机柜起始序号(U)', '设备大小(U)', '资产类型', '资产状态',
                                 '采购公司', '购买时间', '保修到期时间', '是否为自动采集', '备注', '主机名', 'SN号', '管理IP',
                                 '快速服务号', '厂商', '型号', '系统版本', 'CPU型号', 'CPU物理个数', 'CPU逻辑个数', '内存插槽',
                                 '内存SN号', '内存厂商', '内存型号', '内存频率', '内存大小(MB)', '硬盘插槽', '硬盘SN号', '硬盘厂商',
                                 '硬盘型号', '硬盘转速', '硬盘大小(GB)', '网卡插槽', '网卡MAC']
        software_server_title = ['资产ID', '业务线', 'IDC', '资产类型', '资产状态', '是否为自动采集', '备注', '主机名', '系统版本',
                                 'CPU型号', 'CPU物理个数', 'CPU逻辑个数', '内存总大小(MB)', '硬盘总大小(GB)', '网卡名称', '网卡MAC',
                                 '网卡IP']
        network_device_title = ['资产ID', '业务线', 'IDC', '机柜号', '机柜起始序号(U)', '设备大小(U)', '资产类型', '资产状态',
                                '采购公司', '购买时间', '保修到期时间', '是否为自动采集', '备注', '设备名称', '设备类型', 'SN号',
                                '管理IP', '厂商', '型号', '接口数', '基本信息']
        security_device_title = []

        if obj_list:  # 过滤到资产数据了
            file = xlwt.Workbook(encoding='utf-8')
            sheet = file.add_sheet(sheetname='资产明细', cell_overwrite_ok=True)
            row = 0
            for stu in stus:
                col = 0
                for s in stu:
                    sheet.write(row, col, s)
                    col += 1
                row += 1
            file.save(os.path.join(download_dir, '资产明细.xls'))

        return JsonResponse(response.__dict__)
