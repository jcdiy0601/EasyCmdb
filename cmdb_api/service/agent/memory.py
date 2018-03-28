#!/usr/bin/env python
# Author: 'JiaChen'

from utils.response import BaseResponse
from cmdb_data import models
import traceback
from utils import agorithm

# ############# 操作内存信息 #############
# 操作内存，并记录操作日志
# 添加内存
# 删除内存
# 更新内存信息


class HandleMemory(object):
    """
    处理内存信息
    """
    @staticmethod
    def process(server_obj, server_info, user_obj):
        response = BaseResponse()
        try:
            mem_info = server_info['memory']
            if not mem_info['status']:
                models.ErrorLog.objects.create(asset=server_obj.asset, title='memory-run', content=mem_info['error'])
                response.status = False
                return response
            client_mem_dict = mem_info['data']
            mem_obj = models.RAM.objects.filter(asset=server_obj.asset).first()
            if mem_obj:  # 更新
                if mem_obj.total_capacity != client_mem_dict['total_capacity']:
                    log_str = '[更新内存]总容量由%sMB变更为%sMB' % (mem_obj.total_capacity, client_mem_dict['total_capacity'])
                    mem_obj.total_capacity = client_mem_dict['total_capacity']
                    mem_obj.save()
                    models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)
            else:  # 添加
                log_str = '[新增内存]总容量为%sMB' % client_mem_dict['total_capacity']
                models.RAM.objects.create(asset=server_obj.asset, total_capacity=client_mem_dict['total_capacity'])
                models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)
        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(asset=server_obj.asset, title='memory-run', content=traceback.format_exc())
        return response

    @staticmethod
    def _add_memory(add_list, client_mem_dict, server_obj, user_obj):
        for item in add_list:
            cur_mem_dict = client_mem_dict[item]
            log_str = '[新增内存]插槽为{slot};容量为{capacity}MB;类型为{model};厂商为{manufacturer};SN号为{sn}'.format(
                **cur_mem_dict)
            cur_mem_dict['asset'] = server_obj.asset
            models.RAM.objects.create(**cur_mem_dict)
            models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _del_memory(del_list, mem_obj_list, server_obj, user_obj):
        for item in mem_obj_list:
            if item.slot in del_list:
                log_str = '[移除内存]插槽为{slot};容量为{capacity}MB;类型为{model};厂商为{manufacturer};SN号为{sn}'.format(
                    **item.__dict__)
                item.delete()
                models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _update_memory(update_list, mem_obj_list, client_mem_dict, server_obj, user_obj):
        for item in mem_obj_list:
            if item.slot in update_list:
                log_list = []
                new_manufacturer = client_mem_dict[item.slot]['manufacturer']
                if item.manufacturer != new_manufacturer:
                    log_list.append('[更新内存]插槽为%s:厂商由%s变更为%s' % (item.slot, item.manufacturer, new_manufacturer))
                    item.manufacturer = new_manufacturer
                new_model = client_mem_dict[item.slot]['model']
                if item.model != new_model:
                    log_list.append('[更新内存]插槽为%s:型号由%s变更为%s' % (item.slot, item.model, new_model))
                    item.model = new_model
                new_capacity = client_mem_dict[item.slot]['capacity']
                if item.capacity != new_capacity:
                    log_list.append('[更新内存]插槽为%s:容量由%sMB变更为%sMB' % (item.slot, item.capacity, new_capacity))
                    item.capacity = new_capacity
                new_sn = client_mem_dict[item.slot]['sn']
                if item.sn != new_sn:
                    log_list.append('[更新内存]插槽为%s:SN号由%s变更为%s' % (item.slot, item.sn, new_sn))
                    item.sn = new_sn
                item.save()
                if log_list:
                    models.AssetRecord.objects.create(asset=server_obj.asset,
                                                      creator=user_obj,
                                                      content=';'.join(log_list))
