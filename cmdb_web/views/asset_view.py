from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from cmdb_web.service import asset
from django.http import JsonResponse
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
            device_dict['sn'] = form_obj.cleaned_data.pop('sn')
            device_dict['manager_ip'] = form_obj.cleaned_data.pop('manager_ip')
            device_dict['manufacturer'] = form_obj.cleaned_data.pop('manufacturer')
            device_dict['device_type'] = form_obj.cleaned_data.pop('device_type')
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
    if request.method == 'POST':
        if asset_type == 'hardwareserver':
            form_obj = asset_form.AssetEditHardwareServerForm(data=request.POST, initial={'asset_id': asset_id})
            if form_obj.is_valid():
                tag_id_list = form_obj.cleaned_data.pop('tag_id')
                server_dict = {}
                server_dict['manufacturer'] = form_obj.cleaned_data.pop('manufacturer')
                server_dict['hostname'] = form_obj.cleaned_data.pop('hostname')
                server_dict['sn'] = form_obj.cleaned_data.pop('sn')
                server_dict['fast_server_number'] = form_obj.cleaned_data.pop('fast_server_number')
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
                        new_cabinet_order = form_obj.cleaned_data.get('cabinet_order')
                        if not new_cabinet_order:
                            new_cabinet_order = None
                        if asset_obj.cabinet_order:
                            old_cabinet_order = asset_obj.cabinet_order
                        else:
                            old_cabinet_order = None
                        if old_cabinet_order != new_cabinet_order:
                            log_list.append('[更新机柜位置]:由%s变更为%s' % (old_cabinet_order, new_cabinet_order))
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
                            log_list.append('[更新主板厂商]:由%s变更为%s' % (old_manufacturer, new_manufacturer))
                            server_obj.manufacturer = new_manufacturer_id
                        new_hostname = server_dict['hostname']
                        if not new_hostname:
                            new_hostname = None
                        old_hostname = server_obj.hostname
                        if not old_hostname:
                            old_hostname = None
                        if old_hostname != new_hostname:
                            log_list.append('[更新主机名]:由%s变更为%s' % (old_hostname, new_hostname))
                            server_obj.hostname = new_hostname
                        new_sn = server_dict['sn']
                        old_sn = server_obj.sn
                        if old_sn != new_sn:
                            log_list.append('[更新SN号]:由%s变更为%s' % (old_sn, new_sn))
                            server_obj.sn = new_sn
                        new_fast_server_number = server_dict['fast_server_number']
                        if not new_fast_server_number:
                            new_fast_server_number = None
                        old_fast_server_number = server_obj.fast_server_number
                        if not old_fast_server_number:
                            old_fast_server_number = None
                        if old_fast_server_number != new_fast_server_number:
                            log_list.append('[更新快速服务号]:由%s变更为%s' % (old_fast_server_number, new_fast_server_number))
                            server_obj.fast_server_number = new_fast_server_number
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
        if asset_type == 'softwareserver':
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
                        new_cabinet_num = form_obj.cleaned_data.get('cabinet_num')
                        if not new_cabinet_num:
                            new_cabinet_num = None
                        if asset_obj.cabinet_num:
                            old_cabinet_num = asset_obj.cabinet_num
                        else:
                            old_cabinet_num = None
                        if old_cabinet_num != new_cabinet_num:
                            log_list.append('[更新机柜号]:由%s变更为%s' % (old_cabinet_num, new_cabinet_num))
                        new_cabinet_order = form_obj.cleaned_data.get('cabinet_order')
                        if not new_cabinet_order:
                            new_cabinet_order = None
                        if asset_obj.cabinet_order:
                            old_cabinet_order = asset_obj.cabinet_order
                        else:
                            old_cabinet_order = None
                        if old_cabinet_order != new_cabinet_order:
                            log_list.append('[更新机柜位置]:由%s变更为%s' % (old_cabinet_order, new_cabinet_order))
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
        if asset_type == 'networkdevice':
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
                        new_cabinet_order = form_obj.cleaned_data.get('cabinet_order')
                        if not new_cabinet_order:
                            new_cabinet_order = None
                        if asset_obj.cabinet_order:
                            old_cabinet_order = asset_obj.cabinet_order
                        else:
                            old_cabinet_order = None
                        if old_cabinet_order != new_cabinet_order:
                            log_list.append('[更新机柜位置]:由%s变更为%s' % (old_cabinet_order, new_cabinet_order))
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
                            log_list.append('[更新主板厂商]:由%s变更为%s' % (old_manufacturer, new_manufacturer))
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

    elif request.method == 'GET':
        if asset_type == 'hardwareserver':
            form_obj = asset_form.AssetEditHardwareServerForm(initial={'asset_id': asset_id})
        elif asset_type == 'softwareserver':
            form_obj = asset_form.AssetEditSoftwareServerForm(initial={'asset_id': asset_id})
        elif asset_type == 'networkdevice':
            form_obj = asset_form.AssetEditNetworkDeviceForm(initial={'asset_id': asset_id})
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
