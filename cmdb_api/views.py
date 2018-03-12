import json
import importlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.cmdb_api_auth import cmdb_api_auth
from cmdb_api.service import asset
from cmdb_data import models
from cmdb_api import config


@csrf_exempt
@cmdb_api_auth
def asset_api(request):
    """
    API视图
    :param request:
    :return:
    """
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
            for k, v in config.PLUGINS_DICT.items():
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
            sn = server_info['main_board']['data']['sn']
            ret = {'code': 201, 'message': '[%s]更新完成' % sn}
            server_obj = models.HardwareServer.objects.filter(sn=sn).select_related('asset').first()
            if not server_obj:
                ret['code'] = 404
                ret['message'] = '[%s]资产不存在' % sn
                return JsonResponse(ret)
            for k, v in config.PLUGINS_DICT.items():
                module_path, cls_name = v.rsplit('.', 1)
                cls = getattr(importlib.import_module(module_path), cls_name)
                response = cls.process(server_obj, server_info, None)
                if not response.status:
                    ret['code'] = 400
                    ret['message'] = '[%s]资产更新异常' % sn
                if hasattr(cls, 'update_last_time'):
                    cls.update_last_time(server_obj)
            return JsonResponse(ret)
    # 如果请求为get
    response = asset.get_untreated_servers()
    return JsonResponse(response.__dict__)
