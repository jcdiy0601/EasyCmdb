#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from utils.response import BaseResponse
from cmdb_data import models
from cmdb_web.service.base import BaseServiceList
from utils.pager import PageInfo
import json
from cmdb_web.forms.asset_form import AssetUpdateJsonForm


class Asset(BaseServiceList):
    def __init__(self):
        # 查询条件配置
        condition_config = [
            {'name': 'idc_id', 'text': 'IDC机房', 'condition_type': 'select', 'global_name': 'idc_list'},
            {'name': 'asset_type', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'asset_type_list'},
            {'name': 'asset_status', 'text': '资产状态', 'condition_type': 'select', 'global_name': 'asset_status_list'},
            {'name': 'business_unit_id', 'text': '所属业务线', 'condition_type': 'select', 'global_name': 'business_unit_list'}
        ]
        # 表格配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段
                'title': 'ID',  # 前端表格中显示的字段
                'display': 0,   # 是否在前端显示，0为不显示，1为显示
                'text': {'content': '{n}', 'kwargs': {'n': '@id'}},     # 显示内容，字符串表示直接引用，@表示去数据库查询，@@表示特殊处理
                'attr': {}      # 自定义属性
            },
            {
                'q': 'asset_type',
                'title': '资产类型',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@@asset_type_list'}},
                'attr': {}
            },
            {
                'q': 'hostname',
                'title': '主机名/设备名',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@hostname'}},
                'attr': {}
            },
            {
                'q': 'sn',
                'title': 'SN号',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@sn'}},
                'attr': {}
            },
            {
                'q': 'idc_id',
                'title': 'IDC',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@@idc_list'}},
                'attr': {
                    'name': 'idc_id',
                    'id': '@idc_id',
                    'edit-enable': 'true',
                    'edit-type': 'select',
                    'origin': '@idc_id',
                    'global-name': 'idc_list'
                }
            },
            {
                'q': 'business_unit_id',
                'title': '业务线',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@@business_unit_list'}},
                'attr': {
                    'name': 'business_unit_id',
                    'id': '@business_unit_id',
                    'edit-enable': 'true',
                    'edit-type': 'select',
                    'origin': '@business_unit_id',
                    'global-name': 'business_unit_list'
                }
            },
            {
                'q': 'asset_status',
                'title': '资产状态',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@@asset_status_list'}},
                'attr': {
                    'name': 'asset_status',
                    'id': '@asset_status',
                    'edit-enable': 'true',
                    'edit-type': 'select',
                    'origin': '@asset_status',
                    'global-name': 'asset_status_list'
                }
            },
            {
                'q': None,
                'title': '选项',
                'display': 1,
                'text': {
                    'content': '<a href="/cmdb_web/asset_detail_{m}_{n}.html" class="btn btn-xs btn-mint">查看详细</a> | <a href="/cmdb_web/asset_edit_{m}_{n}.html" class="btn btn-xs btn-warning">编辑</a>',
                    'kwargs': {'m': '@asset_type', 'n': '@id'}
                },
                'attr': {}
            }
        ]
        # 额外的查询
        extra_select = {
            'hostname': 'select hostname from cmdb_data_hardwareserver where cmdb_data_hardwareserver.asset_id=cmdb_data_asset.id union all select hostname from cmdb_data_softwareserver where cmdb_data_softwareserver.asset_id=cmdb_data_asset.id union all select device_name from cmdb_data_networkdevice where cmdb_data_networkdevice.asset_id=cmdb_data_asset.id',
            'sn': 'select sn from cmdb_data_hardwareserver where cmdb_data_hardwareserver.asset_id=cmdb_data_asset.id union all select sn from cmdb_data_networkdevice where cmdb_data_networkdevice.asset_id=cmdb_data_asset.id'
        }
        super(Asset, self).__init__(condition_config, table_config, extra_select)

    @property
    def asset_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.asset_type_choices)
        return list(result)     # [{'id': 'hardwareserver', 'name': '硬件服务器'}, {'id': 'softwareserver', 'name': '软件服务器'}]

    @property
    def business_unit_list(self):
        result = models.BusinessUnit.objects.values('id', 'name')
        result = list(result)
        result.insert(0, {'id': None, 'name': None})
        return result           # [{'id': None, 'name': None}, {'id': 1, 'name': '开发组'}, {'id': 2, 'name': '测试组'}]

    @property
    def idc_list(self):
        result = [{'id': None, 'name': None}]
        temp = models.IDC.objects.values_list('id', 'name', 'floor')
        for item in temp:
            result.append({'id': item[0], 'name': '%s-%s层' % (item[1], item[2])})
        return result           # [{'id': None, 'name': None}, {'id': 1, 'name': '大兴世纪互联机房-6层'}]

    @property
    def asset_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.asset_status_choices)
        return list(result)     # [{'id': 'online', 'name': '在线'}, {'id': 'offline', 'name': '离线'}]

    def fetch_asset(self, request):
        """
        获取资产
        :param request:
        :return:
        """
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            asset_count = models.Asset.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.Asset.objects.filter(conditions).extra(select=self.extra_select).values(*self.values_list).order_by('id')[page_info.start:page_info.end]
            """
            <QuerySet [{'id': 1, 'business_unit_id': None, 'asset_status': 'online', 'asset_type': 'server', 'idc_id': 1, 'server_title': 'ytd13'}, {'id': 2, 'business_unit_id': None, 'asset_sta
tus': 'online', 'asset_type': 'server', 'idc_id': None, 'server_title': 'CentOS-01'}]>
            """
            # 加入查询条件
            ret['condition_config'] = self.condition_config
            # 加入配置文件
            ret['table_config'] = self.table_config
            # 加入查询到的数据
            ret['data_list'] = list(asset_list)
            # 加入页面信息
            ret['page_info'] = {
                'page_str': page_info.pager(),
                'page_start': page_info.start,
            }
            # 加入全局变量
            ret['global_dict'] = {
                'asset_type_list': self.asset_type_list,
                'business_unit_list': self.business_unit_list,
                'idc_list': self.idc_list,
                'asset_status_list': self.asset_status_list
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def delete_asset(request):
        """
        删除资产
        :param request:
        :return:
        """
        response = BaseResponse()
        try:
            id_list = request.POST.getlist('id_list')
            for nid in id_list:
                asset_obj = models.Asset.objects.get(id=nid)
                asset_obj.delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def update_asset(request):
        """
        更新资产
        :param request:
        :return:
        """
        response = BaseResponse()
        response.error = []
        update_str = request.POST.get('update_list')
        update_list = json.loads(update_str)
        error_count = 0
        for row_dict in update_list:
            nid = row_dict['nid']
            num = row_dict['num']
            del row_dict['nid']
            del row_dict['num']
            form_obj = AssetUpdateJsonForm(row_dict)
            # 字段全部验证正确
            if form_obj.is_valid():
                log_list = []
                asset_obj = models.Asset.objects.get(id=nid)
                # row_dict中只有asset_status情况
                if len(row_dict) == 1 and 'asset_status' in row_dict:
                    form_obj.cleaned_data.pop('business_unit_id')
                    form_obj.cleaned_data.pop('idc_id')
                    asset_status_choices = asset_obj.asset_status_choices
                    new_asset_status_id = form_obj.cleaned_data.get('asset_status')
                    for item in asset_status_choices:
                        if item[0] == new_asset_status_id:
                            new_asset_status = item[1]
                            break
                    old_asset_status_id = asset_obj.asset_status
                    for item in asset_status_choices:
                        if item[0] == old_asset_status_id:
                            old_asset_status = item[1]
                            break
                    log_list.append('[更新资产状态]:由%s变更为%s' % (old_asset_status, new_asset_status))
                    models.Asset.objects.filter(id=nid).update(**form_obj.cleaned_data)
                    user_obj = request.user
                    models.AssetRecord.objects.create(asset=asset_obj, creator=user_obj, content=';'.join(log_list))
                else:
                    if 'business_unit_id' in row_dict:
                        new_business_unit_id = form_obj.cleaned_data.get('business_unit_id')
                        if new_business_unit_id:
                            new_business_unit = models.BusinessUnit.objects.filter(id=new_business_unit_id).first().name
                        else:
                            new_business_unit = None
                        if asset_obj.business_unit:
                            old_business_unit = asset_obj.business_unit.name
                        else:
                            old_business_unit = None
                        if old_business_unit != new_business_unit:
                            log_list.append('[更新业务线]:由%s变更为%s' % (old_business_unit, new_business_unit))
                    else:
                        form_obj.cleaned_data.pop('business_unit_id')
                    if 'idc_id' in row_dict:
                        new_idc_id = form_obj.cleaned_data.get('idc_id')
                        if new_idc_id:
                            new_idc = models.IDC.objects.filter(id=new_idc_id).first().name
                        else:
                            new_idc = None
                        if asset_obj.idc:
                            old_idc = asset_obj.idc.name
                        else:
                            old_idc = None
                        if old_idc != new_idc:
                            log_list.append('[更新IDC]:由%s变更为%s' % (old_idc, new_idc))
                    else:
                        form_obj.cleaned_data.pop('idc_id')
                    asset_status_choices = asset_obj.asset_status_choices
                    new_asset_status_id = form_obj.cleaned_data.get('asset_status')
                    for item in asset_status_choices:
                        if item[0] == new_asset_status_id:
                            new_asset_status = item[1]
                            break
                    old_asset_status_id = asset_obj.asset_status
                    for item in asset_status_choices:
                        if item[0] == old_asset_status_id:
                            old_asset_status = item[1]
                            break
                    log_list.append('[更新资产状态]:由%s变更为%s' % (old_asset_status, new_asset_status))
                    models.Asset.objects.filter(id=nid).update(**form_obj.cleaned_data)
                    user_obj = request.user
                    models.AssetRecord.objects.create(asset=asset_obj, creator=user_obj, content=';'.join(log_list))
            # 字段非全部验证正确
            else:
                flag_tag = False
                message = ''
                for key in row_dict:
                    # 被验证字段在错误信息中
                    if key in json.loads(form_obj.errors.as_json()):
                        if not message:
                            message = json.loads(form_obj.errors.as_json())[key][0]['message']
                        else:
                            message = message + '&' + json.loads(form_obj.errors.as_json())[key][0]['message']
                        flag_tag = True
                response.error.append({'num': num, 'message': message})
                if not flag_tag:
                    log_list = []
                    asset_obj = models.Asset.objects.get(id=nid)
                    if 'business_unit_id' in row_dict:
                        new_business_unit_id = row_dict.get('business_unit_id')
                        if new_business_unit_id:
                            new_business_unit = models.BusinessUnit.objects.filter(id=new_business_unit_id).first().name
                        else:
                            new_business_unit = None
                        if asset_obj.business_unit:
                            old_business_unit = asset_obj.business_unit.name
                        else:
                            old_business_unit = None
                        log_list.append('[更新业务线]:由%s变更为%s' % (old_business_unit, new_business_unit))
                    if 'idc_id' in row_dict:
                        new_idc_id = row_dict.get('idc_id')
                        if new_idc_id:
                            new_idc = models.IDC.objects.filter(id=new_idc_id).first().name
                        else:
                            new_idc = None
                        if asset_obj.idc:
                            old_idc = asset_obj.idc.name
                        else:
                            old_idc = None
                        log_list.append('[更新IDC]:由%s变更为%s' % (old_idc, new_idc))
                    models.Asset.objects.filter(id=nid).update(**row_dict)
                    user_obj = request.user
                    models.AssetRecord.objects.create(asset=asset_obj, creator=user_obj, content=';'.join(log_list))
                else:
                    response.status = False
                    error_count += 1
        if error_count:
            response.message = '共%s条,失败%s条' % (len(update_list), error_count)
        else:
            response.message = '更新成功'
        return response

    @staticmethod
    def asset_detail(asset_id):
        response = BaseResponse()
        try:
            response.data = models.Asset.objects.filter(id=asset_id).first()
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response
