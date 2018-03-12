#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from utils.response import BaseResponse
from cmdb_data import models
import traceback
import datetime
from utils import agorithm


def get_untreated_servers():
    """
    获取在线的硬件服务器信息
    :return:
    """
    response = BaseResponse()
    try:
        result = models.HardwareServer.objects.filter(asset__asset_status='online').values('manager_ip')
        response.data = list(result)
    except Exception as e:
        response.message = str(e)
        response.status = False
        models.ErrorLog.objects.create(asset=None, title='get_untreated_servers', content=traceback.format_exc())
    return response


# ############# 操作基本信息（cpu和主板） #############
# 操作基本，并记录操作日志
# 更新cpu和主板信息


class HandleBasic(object):
    """
    处理基本信息，包括主板和CPU信息
    """

    @staticmethod
    def process(server_obj, server_info, user_obj):
        response = BaseResponse()
        if server_obj.asset.asset_type == 'softwareserver':
            try:
                log_list = []
                cpu = server_info['cpu']['data']
                cpu_obj = models.CPU.objects.filter(asset=server_obj.asset).first()
                if server_obj.os_version != server_info['os_version']:
                    log_list.append('系统版本由%s变更为%s' % (server_obj.os_version, server_info['os_version']))
                    server_obj.os_version = server_info['os_version']
                if not cpu_obj:
                    models.CPU.objects.create(asset=server_obj.asset,
                                              cpu_model=cpu['cpu_model'],
                                              cpu_physical_count=cpu['cpu_physical_count'],
                                              cpu_count=cpu['cpu_count'])
                    log_list.append(
                        '[新增CPU]型号为%s;物理数为%s;逻辑数为%s' % (cpu['cpu_model'], cpu['cpu_physical_count'], cpu['cpu_count']))
                else:
                    if cpu_obj.cpu_count != cpu['cpu_count']:
                        log_list.append('CPU逻辑核数由%s变更为%s' % (cpu_obj.cpu_count, cpu['cpu_count']))
                        cpu_obj.cpu_count = cpu['cpu_count']
                    if cpu_obj.cpu_model != cpu['cpu_model']:
                        log_list.append('CPU型号由%s变更为%s' % (cpu_obj.cpu_model, cpu['cpu_model']))
                        cpu_obj.cpu_model = cpu['cpu_model']
                    if cpu_obj.cpu_physical_count != cpu['cpu_physical_count']:
                        log_list.append('CPU物理数由%s变更为%s' % (cpu_obj.cpu_physical_count, cpu['cpu_physical_count']))
                        cpu_obj.cpu_physical_count = cpu['cpu_physical_count']
                    cpu_obj.save()
                server_obj.save()
                if log_list:
                    models.AssetRecord.objects.create(asset=server_obj.asset,
                                                      content=';'.join(log_list),
                                                      creator=user_obj)
            except Exception as e:
                response.status = False
                models.ErrorLog.objects.create(asset=server_obj.asset, title='basic-run',
                                               content=traceback.format_exc())
            return response
        if server_obj.asset.asset_type == 'hardwareserver':
            try:
                log_list = []
                main_board = server_info['main_board']['data']
                cpu = server_info['cpu']['data']
                cpu_obj = models.CPU.objects.filter(asset=server_obj.asset).first()
                if server_obj.os_version != server_info['os_version']:
                    log_list.append('系统版本由%s变更为%s' % (server_obj.os_version, server_info['os_version']))
                    server_obj.os_version = server_info['os_version']
                if server_obj.hostname != server_info['hostname']:
                    log_list.append('系统主机名由%s变更为%s' % (server_obj.hostname, server_info['hostname']))
                    server_obj.hostname = server_info['hostname']
                if server_obj.sn != main_board['sn']:
                    log_list.append('主板SN号由%s变更为%s' % (server_obj.sn, main_board['sn']))
                    server_obj.sn = main_board['sn']
                if server_obj.fast_server_number != main_board['fast_server_number']:
                    log_list.append(
                        '主板快速服务号由%s变更为%s' % (server_obj.fast_server_number, main_board['fast_server_number']))
                    server_obj.fast_server_number = main_board['fast_server_number']
                if server_obj.manufacturer != main_board['manufacturer']:
                    log_list.append('主板厂商由%s变更为%s' % (server_obj.manufacturer, main_board['manufacturer']))
                    server_obj.manufacturer = main_board['manufacturer']
                if server_obj.model != main_board['model']:
                    log_list.append('主板型号由%s变更为%s' % (server_obj.model, main_board['model']))
                    server_obj.model = main_board['model']
                if not cpu_obj:
                    models.CPU.objects.create(asset=server_obj.asset,
                                              cpu_model=cpu['cpu_model'],
                                              cpu_physical_count=cpu['cpu_physical_count'],
                                              cpu_count=cpu['cpu_count'])
                    log_list.append('[新增CPU]型号为%s;物理数为%s;逻辑数为%s' % (cpu['cpu_model'], cpu['cpu_physical_count'], cpu['cpu_count']))
                else:
                    if cpu_obj.cpu_count != cpu['cpu_count']:
                        log_list.append('CPU逻辑核数由%s变更为%s' % (cpu_obj.cpu_count, cpu['cpu_count']))
                        cpu_obj.cpu_count = cpu['cpu_count']
                    if cpu_obj.cpu_model != cpu['cpu_model']:
                        log_list.append('CPU型号由%s变更为%s' % (cpu_obj.cpu_model, cpu['cpu_model']))
                        cpu_obj.cpu_model = cpu['cpu_model']
                    if cpu_obj.cpu_physical_count != cpu['cpu_physical_count']:
                        log_list.append('CPU物理数由%s变更为%s' % (cpu_obj.cpu_physical_count, cpu['cpu_physical_count']))
                        cpu_obj.cpu_physical_count = cpu['cpu_physical_count']
                    cpu_obj.save()
                server_obj.save()
                if log_list:
                    models.AssetRecord.objects.create(asset=server_obj.asset,
                                                      content=';'.join(log_list),
                                                      creator=user_obj)
            except Exception as e:
                response.status = False
                models.ErrorLog.objects.create(asset=server_obj.asset, title='basic-run',
                                               content=traceback.format_exc())
            return response

    @staticmethod
    def update_last_time(server_obj):
        """
        :param server_obj:
        :param user_obj:
        :return:
        """
        response = BaseResponse()
        try:
            current_date = datetime.date.today()
            server_obj.asset.latest_date = current_date
            server_obj.asset.save()
        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(asset_obj=server_obj.asset, title='basic-run',
                                           content=traceback.format_exc())
        return response


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
            if server_obj.asset.asset_type == 'softwareserver':  # 软件服务器
                nic_name_list = [item.name for item in nic_obj_list]
                update_list = agorithm.get_intersection(set(client_nic_dict.keys()), set(nic_name_list))
                add_list = agorithm.get_exclude(client_nic_dict.keys(), update_list)
                del_list = agorithm.get_exclude(nic_name_list, update_list)
            elif server_obj.asset.asset_type == 'hardwareserver':  # 硬件服务器
                nic_slot_list = [item.slot for item in nic_obj_list]
                update_list = agorithm.get_intersection(set(client_nic_dict.keys()), set(nic_slot_list))
                add_list = agorithm.get_exclude(client_nic_dict.keys(), update_list)
                del_list = agorithm.get_exclude(nic_slot_list, update_list)
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
            if server_obj.asset.asset_type == 'softwareserver':  # 软件服务器
                cur_nic_dict['name'] = item
                log_str = '[新增网卡]{name}:mac地址为{macaddress};IP地址为{ipaddress}'.format(**cur_nic_dict)
                cur_nic_dict['asset'] = server_obj.asset
                models.NIC.objects.create(**cur_nic_dict)
                models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)
            elif server_obj.asset.asset_type == 'hardwareserver':  # 硬件服务器
                cur_nic_dict['slot'] = item
                log_str = '[新增网卡]{slot}:mac地址为{macaddress}'.format(**cur_nic_dict)
                cur_nic_dict['asset'] = server_obj.asset
                models.NIC.objects.create(**cur_nic_dict)
                models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _del_nic(del_list, nic_obj_list, server_obj, user_obj):
        for item in nic_obj_list:
            if server_obj.asset.asset_type == 'softwareserver':  # 软件服务器
                if item.name in del_list:
                    log_str = '[移除网卡]{name}:mac地址为{macaddress};IP地址为{ipaddress}'.format(**item.__dict__)
                    item.delete()
                    models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)
            elif server_obj.asset.asset_type == 'hardwareserver':  # 硬件服务器
                if item.slot in del_list:
                    log_str = '[移除网卡]{slot}:mac地址为{macaddress}'.format(**item.__dict__)
                    item.delete()
                    models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)

    @staticmethod
    def _update_nic(update_list, nic_obj_list, client_nic_dict, server_obj, user_obj):
        for item in nic_obj_list:
            if server_obj.asset.asset_type == 'softwareserver':  # 软件服务器
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
            elif server_obj.asset.asset_type == 'hardwareserver':  # 硬件服务器
                if item.slot in update_list:
                    log_list = []
                    new_macaddress = client_nic_dict[item.slot]['macaddress']
                    if item.macaddress != new_macaddress:
                        log_list.append('[更新网卡]%s:mac地址由%s变更为%s' % (item.slot, item.macaddress, new_macaddress))
                        item.macaddress = new_macaddress
                    item.save()
                    if log_list:
                        models.AssetRecord.objects.create(asset=server_obj.asset,
                                                          creator=user_obj,
                                                          content=';'.join(log_list))


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
            if server_obj.asset.asset_type == 'softwareserver':  # 软件服务器
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
            elif server_obj.asset.asset_type == 'hardwareserver':  # 硬件服务器
                mem_obj_list = models.RAM.objects.filter(asset=server_obj.asset)
                mem_slot_list = [item.slot for item in mem_obj_list]
                update_list = agorithm.get_intersection(set(client_mem_dict.keys()), set(mem_slot_list))
                add_list = agorithm.get_exclude(client_mem_dict.keys(), update_list)
                del_list = agorithm.get_exclude(mem_slot_list, update_list)
                HandleMemory._add_memory(add_list, client_mem_dict, server_obj, user_obj)
                HandleMemory._del_memory(del_list, mem_obj_list, server_obj, user_obj)
                HandleMemory._update_memory(update_list, mem_obj_list, client_mem_dict, server_obj, user_obj)
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
            if server_obj.asset.asset_type == 'softwareserver':  # 软件服务器
                disk_obj = models.Disk.objects.filter(asset=server_obj.asset).first()
                if disk_obj:  # 更新
                    if disk_obj.total_capacity != client_disk_dict['total_capacity']:
                        log_str = '[更新硬盘]总容量由%sG变更为%sG' % (disk_obj.total_capacity, client_disk_dict['total_capacity'])
                        disk_obj.total_capacity = client_disk_dict['total_capacity']
                        disk_obj.save()
                        models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)
                else:  # 添加
                    log_str = '[新增硬盘]总容量为%sG' % client_disk_dict['total_capacity']
                    models.Disk.objects.create(asset=server_obj.asset,
                                               total_capacity=client_disk_dict['total_capacity'])
                    models.AssetRecord.objects.create(asset=server_obj.asset, creator=user_obj, content=log_str)
            elif server_obj.asset.asset_type == 'hardwareserver':  # 硬件服务器
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
