#!/usr/bin/env python
# Author: 'JiaChen'

from utils.response import BaseResponse
from cmdb_data import models
import traceback
import datetime


class HandleBasic(object):
    """
    处理交换机基本信息
    """
    @staticmethod
    def process(device_obj, device_info, user_obj):
        response = BaseResponse()
        try:
            log_list = []
            basic_info_dict = device_info['basic']['data']
            if device_obj.port_number != basic_info_dict['port_number']:
                log_list.append('接口数由%s变更为%s' % (device_obj.port_number, basic_info_dict['port_number']))
                device_obj.port_number = basic_info_dict['port_number']
            if device_obj.run_time != basic_info_dict['run_time']:
                log_list.append('运行时间由%s变更为%s' % (device_obj.run_time, basic_info_dict['run_time']))
                device_obj.run_time = basic_info_dict['run_time']
            if device_obj.device_name != basic_info_dict['device_name']:
                log_list.append('设备名称由%s变更为%s' % (device_obj.device_name, basic_info_dict['device_name']))
                device_obj.device_name = basic_info_dict['device_name']
            if device_obj.model != basic_info_dict['model']:
                log_list.append('型号由%s变更为%s' % (device_obj.model, basic_info_dict['model']))
                device_obj.model = basic_info_dict['model']
            if device_obj.basic_info != basic_info_dict['basic_info']:
                log_list.append('型号由%s变更为%s' % (device_obj.basic_info, basic_info_dict['basic_info']))
                device_obj.basic_info = basic_info_dict['basic_info']
            device_obj.save()
            if log_list:
                models.AssetRecord.objects.create(asset=device_obj.asset,
                                                  content=';'.join(log_list),
                                                  creator=user_obj)
        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(asset=device_obj.asset, title='basic-run',
                                           content=traceback.format_exc())
        return response

    @staticmethod
    def update_last_time(device_obj):
        """
        :param device_obj:
        :param user_obj:
        :return:
        """
        response = BaseResponse()
        try:
            current_date = datetime.date.today()
            device_obj.asset.latest_date = current_date
            device_obj.asset.save()
        except Exception as e:
            response.status = False
            models.ErrorLog.objects.create(asset_obj=device_obj.asset, title='basic-run',
                                           content=traceback.format_exc())
        return response
