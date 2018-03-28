#!/usr/bin/env python
# Author: 'JiaChen'

from utils.response import BaseResponse
from cmdb_data import models
import traceback
from utils import agorithm

# ############# 操作硬盘信息 #############
# 操作硬盘，并记录操作日志
# 添加硬盘
# 删除硬盘
# 更新硬盘信息


class HandleDisk(object):
    """
    处理硬盘信息
    """

    @staticmethod
    def process(server_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            disk_info = server_info['disk']
            if not disk_info['status']:
                response.status = False
                models.ErrorLog.objects.create(asset=server_obj.asset, title='disk-agent', content=disk_info['error'])
                return response
            client_disk_dict = disk_info['data']
            disk_obj_list = models.Disk.objects.filter(asset=server_obj.asset)
            disk_slot_list = [item.slot for item in disk_obj_list]
            update_list = agorithm.get_intersection(set(client_disk_dict.keys()), set(disk_slot_list))
            add_list = agorithm.get_exclude(client_disk_dict.keys(), update_list)
            del_list = agorithm.get_exclude(disk_slot_list, update_list)
            HandleDisk._add_disk(add_list, client_disk_dict, server_obj, user_obj)
            HandleDisk._del_disk(del_list, disk_obj_list, server_obj, user_obj)
            HandleDisk._update_disk(update_list, disk_obj_list, client_disk_dict, server_obj, user_obj)
        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(asset=server_obj.asset, title='disk-run', content=traceback.format_exc())
        return response

    @staticmethod
    def _add_disk(add_list, client_disk_dict, server_obj, user_obj):
        for item in add_list:
            cur_disk_dict = client_disk_dict[item]
            log_str = '[新增硬盘]插槽为{slot};容量为{capacity}GB;厂商为{manufacturer};型号为{model};SN号为{sn}'.format(**cur_disk_dict)
            cur_disk_dict['asset'] = server_obj.asset
            models.Disk.objects.create(**cur_disk_dict)
            models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _del_disk(del_list, disk_obj_list, server_obj, user_obj):
        for item in disk_obj_list:
            if item.slot in del_list:
                log_str = '[移除硬盘]插槽为{slot};容量为{capacity}GB;厂商为{manufacturer};型号为{model};SN号为{sn}'.format(
                    **item.__dict__)
                item.delete()
                models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _update_disk(update_list, disk_obj_list, client_disk_dict, server_obj, user_obj):
        for item in disk_obj_list:
            if item.slot in update_list:
                log_list = []
                new_model = client_disk_dict[item.slot]['model']
                if item.model != new_model:
                    log_list.append('[更新硬盘]插槽为%s:型号由%s变更为%s' % (item.slot, item.model, new_model))
                    item.model = new_model
                new_sn = client_disk_dict[item.slot]['sn']
                if item.sn != new_sn:
                    log_list.append('[更新硬盘]插槽为%s:SN号由%s变更为%s' % (item.slot, item.sn, new_sn))
                    item.sn = new_sn
                new_capacity = client_disk_dict[item.slot]['capacity']
                if item.capacity != new_capacity:
                    log_list.append('[更新硬盘]插槽为%s:容量由%sG变更为%sG' % (item.slot, item.capacity, new_capacity))
                    item.capacity = new_capacity
                new_manufacturer = client_disk_dict[item.slot]['manufacturer']
                if item.manufacturer != new_manufacturer:
                    log_list.append('[更新硬盘]插槽为%s:厂商由%s变更为%s' % (item.slot, item.manufacturer, new_manufacturer))
                    item.manufacturer = new_manufacturer
                item.save()
                if log_list:
                    models.AssetRecord.objects.create(asset=server_obj.asset,
                                                      creator=user_obj,
                                                      content=';'.join(log_list))
