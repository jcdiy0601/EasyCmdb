#!/usr/bin/env python
# Author: 'JiaChen'

from utils.response import BaseResponse
from cmdb_data import models
import traceback
from utils import agorithm

# ############# 操作网卡信息 #############
# 操作网卡，并记录操作日志
# 添加网卡
# 删除网卡
# 更新网卡信息


class HandleNic(object):
    """
    处理网卡信息
    """
    @staticmethod
    def process(server_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            nic_info = server_info['nic']
            if not nic_info['status']:
                response.status = False
                models.ErrorLog.objects.create(asset=server_obj.asset, title='nic-run', content=nic_info['error'])
                return response
            client_nic_dict = nic_info['data']
            nic_obj_list = models.NIC.objects.filter(asset=server_obj.asset)
            nic_name_list = [item.name for item in nic_obj_list]
            update_list = agorithm.get_intersection(set(client_nic_dict.keys()), set(nic_name_list))
            add_list = agorithm.get_exclude(client_nic_dict.keys(), update_list)
            del_list = agorithm.get_exclude(nic_name_list, update_list)
            HandleNic._add_nic(add_list, client_nic_dict, server_obj, user_obj)
            HandleNic._del_nic(del_list, nic_obj_list, server_obj, user_obj)
            HandleNic._update_nic(update_list, nic_obj_list, client_nic_dict, server_obj, user_obj)
        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(asset=server_obj.asset, title='nic-run', content=traceback.format_exc())
        return response

    @staticmethod
    def _add_nic(add_list, client_nic_dict, server_obj, user_obj):
        for item in add_list:
            cur_nic_dict = client_nic_dict[item]
            cur_nic_dict['name'] = item
            log_str = '[新增网卡]{name}:mac地址为{macaddress};IP地址为{ipaddress}'.format(**cur_nic_dict)
            cur_nic_dict['asset'] = server_obj.asset
            models.NIC.objects.create(**cur_nic_dict)
            models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _del_nic(del_list, nic_obj_list, server_obj, user_obj):
        for item in nic_obj_list:
            if item.name in del_list:
                log_str = '[移除网卡]{name}:mac地址为{macaddress};IP地址为{ipaddress}'.format(**item.__dict__)
                item.delete()
                models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _update_nic(update_list, nic_obj_list, client_nic_dict, server_obj, user_obj):
        for item in nic_obj_list:
            if item.name in update_list:
                log_list = []
                new_macaddress = client_nic_dict[item.name]['macaddress']
                if item.macaddress != new_macaddress:
                    log_list.append('[更新网卡]%s:mac地址由%s变更为%s' % (item.name, item.macaddress, new_macaddress))
                    item.macaddress = new_macaddress
                new_ipaddress = client_nic_dict[item.name]['ipaddress']
                if item.ipaddress != new_ipaddress:
                    log_list.append('[更新网卡]%s:IP地址由%s变更为%s' % (item.name, item.ipaddress, new_ipaddress))
                    item.ipaddress = new_ipaddress
                item.save()
                if log_list:
                    models.AssetRecord.objects.create(asset=server_obj.asset,
                                                      creator=user_obj,
                                                      content=';'.join(log_list))
