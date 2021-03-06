import json
import importlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.cmdb_api_auth import cmdb_api_auth
from cmdb_api.service import asset
from cmdb_api.service import softwareserver
from cmdb_api.service import monitor
from cmdb_data import models
from cmdb_api import config
from utils.response import BaseResponse
import traceback


@csrf_exempt
@cmdb_api_auth
def asset_api(request):
    """资产API视图"""
    # 如果请求为post
    if request.method == 'POST':
        server_info = json.loads(request.body.decode('utf-8'))
        server_info = json.loads(server_info)
        hostname = server_info.get('hostname', None)
        client_type = server_info['client_type']
        # 如果资产由agent获取
        if client_type == 'agent':
            ret = {'code': 201, 'message': '[%s]更新完成' % hostname}
            server_obj = models.SoftwareServer.objects.filter(hostname=hostname).select_related('asset').first()
            if not server_obj:
                ret['code'] = 404
                ret['message'] = '[%s]资产不存在' % hostname
                return JsonResponse(ret)
            for k, v in config.PLUGINS_AGENT_DICT.items():
                module_path, cls_name = v.rsplit('.', 1)
                cls = getattr(importlib.import_module(module_path), cls_name)
                response = cls.process(server_obj, server_info, None)
                if not response.status:
                    ret['code'] = 400
                    ret['message'] = '[%s]资产更新异常' % hostname
                if hasattr(cls, 'update_last_time'):
                    cls.update_last_time(server_obj)
            return JsonResponse(ret)
        # 如果资产由snmp获取
        elif client_type == 'snmp':
            device_type = server_info['device_type']
            if device_type == 'server':     # 硬件服务器
                sn = server_info['main_board']['data']['sn']
                ret = {'code': 201, 'message': '[%s]更新完成' % sn}
                server_obj = models.HardwareServer.objects.filter(sn=sn).select_related('asset').first()
                if not server_obj:
                    ret['code'] = 404
                    ret['message'] = '[%s]资产不存在' % sn
                    return JsonResponse(ret)
                server_plugin_dict = config.PLUGINS_SNMP_DICT[device_type]
                for k, v in server_plugin_dict.items():
                    module_path, cls_name = v.rsplit('.', 1)
                    cls = getattr(importlib.import_module(module_path), cls_name)
                    response = cls.process(server_obj, server_info, None)
                    if not response.status:
                        ret['code'] = 400
                        ret['message'] = '[%s]资产更新异常' % sn
                    if hasattr(cls, 'update_last_time'):
                        cls.update_last_time(server_obj)
                return JsonResponse(ret)
            elif device_type == 'switch':
                sn = server_info['basic']['data']['sn']
                ret = {'code': 201, 'message': '[%s]更新完成' % sn}
                device_obj = models.NetworkDevice.objects.filter(sn=sn).select_related('asset').first()
                if not device_obj:
                    ret['code'] = 404
                    ret['message'] = '[%s]资产不存在' % sn
                    return JsonResponse(ret)
                device_plugin_dict = config.PLUGINS_SNMP_DICT[device_type]
                for k, v in device_plugin_dict.items():
                    module_path, cls_name = v.rsplit('.', 1)
                    cls = getattr(importlib.import_module(module_path), cls_name)
                    response = cls.process(device_obj, server_info, None)
                    if not response.status:
                        ret['code'] = 400
                        ret['message'] = '[%s]资产更新异常' % sn
                    if hasattr(cls, 'update_last_time'):
                        cls.update_last_time(device_obj)
                return JsonResponse(ret)
            elif device_type == 'firewall':
                sn = server_info['basic']['data']['sn']
                ret = {'code': 201, 'message': '[%s]更新完成' % sn}
                device_obj = models.NetworkDevice.objects.filter(sn=sn).select_related('asset').first()
                if not device_obj:
                    ret['code'] = 404
                    ret['message'] = '[%s]资产不存在' % sn
                    return JsonResponse(ret)
                device_plugin_dict = config.PLUGINS_SNMP_DICT[device_type]
                for k, v in device_plugin_dict.items():
                    module_path, cls_name = v.rsplit('.', 1)
                    cls = getattr(importlib.import_module(module_path), cls_name)
                    response = cls.process(device_obj, server_info, None)
                    if not response.status:
                        ret['code'] = 400
                        ret['message'] = '[%s]资产更新异常' % sn
                    if hasattr(cls, 'update_last_time'):
                        cls.update_last_time(device_obj)
                return JsonResponse(ret)
    # 如果请求为get
    response = asset.get_untreated_servers()
    return JsonResponse(response.__dict__)


@csrf_exempt
@cmdb_api_auth
def softwareserver_basic_info_api(request):
    """软件服务器获取基础信息API视图"""
    response = BaseResponse()
    ret = {'idc': {}, 'business_unit': {}}
    idc = models.IDC.objects.all()
    for idc_obj in idc:
        ret['idc'][idc_obj.id] = '%s-%s' % (idc_obj.name, idc_obj.floor)
    business_unit = models.BusinessUnit.objects.all()
    for business_unit_obj in business_unit:
        ret['business_unit'][business_unit_obj.id] = business_unit_obj.name
    response.data = ret
    return JsonResponse(response.__dict__)


@csrf_exempt
@cmdb_api_auth
def softwareserver_api(request):
    """软件服务器API视图"""
    if request.method == 'POST':
        response = BaseResponse()
        report_data = json.loads(request.body.decode('utf-8'))
        hostname = report_data.get('hostname', None)
        idc = report_data.get('idc', None)
        business_unit = report_data.get('business_unit', None)
        if not idc:
            response.status = False
            response.message = '未提供IDC信息'
            return JsonResponse(response.__dict__)
        if not business_unit:
            response.status = False
            response.message = '未提供业务线信息'
            return JsonResponse(response.__dict__)
        if hostname:
            host_obj = models.SoftwareServer.objects.filter(hostname=hostname).first()
            if host_obj:
                response.status = False
                response.message = '此软件服务器的主机名已存在'
                return JsonResponse(response.__dict__)
            else:
                try:
                    asset_obj = models.Asset.objects.create(idc_id=int(idc),
                                                            business_unit_id=int(business_unit),
                                                            cabinet_num='',
                                                            cabinet_order='')
                    models.SoftwareServer.objects.create(asset=asset_obj, hostname=hostname)
                    response.message = '软件服务器资产添加成功'
                    return JsonResponse(response.__dict__)
                except Exception as e:
                    response.message = '软件服务器资产添加失败'
                    response.error = str(e)
                    response.status = False
                    models.ErrorLog.objects.create(asset=None, title='save_softwareserver_api_post_data',
                                                   content=traceback.format_exc())
                    return JsonResponse(response.__dict__)
        else:
            response.status = False
            response.message = '未提供软件服务器主机名'
            return JsonResponse(response.__dict__)
    # 如果请求为get
    hostname = request.GET.get('hostname', None)
    if hostname:
        response = softwareserver.check_softwareserver_exist(hostname=hostname)
    else:
        response = BaseResponse()
        response.status = False
        response.message = '未提供软件服务器主机名'
    return JsonResponse(response.__dict__)


# @csrf_exempt
# @cmdb_api_auth
# def monitor_api(request):
#     """监控api"""
#     if request.method == 'POST':
#         pass
#     # 如果请求为get
#     hostname = request.GET.get('hostname', None)
#     if hostname:
#         response = monitor.check_hostname_exit(hostname=hostname)
#     else:
#         response = BaseResponse()
#         response.status = False
#         response.message = '未提供软件服务器主机名'
#     return JsonResponse(response.__dict__)
