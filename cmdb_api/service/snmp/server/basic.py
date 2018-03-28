#!/usr/bin/env python
# Author: 'JiaChen'

from utils.response import BaseResponse
from cmdb_data import models
import traceback
import datetime

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
