#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from utils.response import BaseResponse
from cmdb_data import models
from cmdb_web.service.base import BaseServiceList
from utils.pager import PageInfo
import json
from cmdb_web.forms.business_unit_form import BusinessUnitUpdateJsonForm


class BusinessUnit(BaseServiceList):
    def __init__(self):
        # 查询条件配置
        condition_config = [
            {'name': 'name', 'text': '业务线名称', 'condition_type': 'input'},
        ]
        # 表格配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段
                'title': 'ID',  # 前端表格中显示的字段
                'display': 0,  # 是否在前端显示，0为不显示，1为显示
                'text': {'content': '{n}', 'kwargs': {'n': '@id'}},  # 显示内容，字符串表示直接引用，@开头表示去数据库查询，@@表示特殊处理
                'attr': {},  # 自定义属性
            },
            {
                'q': 'name',
                'title': '业务线名称',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@name'}},
                'attr': {'name': 'name',
                         'edit-enable': 'true',
                         'edit-type': 'input',
                         'origin': '@name'}
            },
            {
                'q': 'contact_id',
                'title': '联系人',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@@contact_list'}},
                'attr': {'name': 'contact_id',
                         'id': '@contact_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'origin': '@contact_id',
                         'global-name': 'contact_list'}
            },
            {
                'q': 'manager_id',
                'title': '管理人',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@@manager_list'}},
                'attr': {'name': 'manager_id',
                         'id': '@manager_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'origin': '@manager_id',
                         'global-name': 'manager_list'}
            }
        ]
        # 额外搜索条件
        extra_select = {}
        super(BusinessUnit, self).__init__(condition_config, table_config, extra_select)

    @property
    def contact_list(self):
        """
        URL类型列表
        :return:
        """
        values = models.UserProfile.objects.values('id', 'name')
        for value in values:
            value['name'] = value['name']
        result = list(values)
        return list(result)

    @property
    def manager_list(self):
        """
        请求类型列表
        :return:
        """
        values = models.UserProfile.objects.values('id', 'name')
        for value in values:
            value['name'] = value['name']
        result = list(values)
        return list(result)

    def fetch_business_unit(self, request):
        """
        获取业务线信息
        :param request:
        :return:
        """
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            business_unit_count = models.BusinessUnit.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), business_unit_count)
            business_unit_list = models.BusinessUnit.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list).order_by('id')[page_info.start:page_info.end]
            # 加入查询条件
            ret['condition_config'] = self.condition_config
            # 加入配置文件
            ret['table_config'] = self.table_config
            # 加入查询到的数据
            ret['data_list'] = list(business_unit_list)
            # 加入页面信息
            ret['page_info'] = {
                'page_str': page_info.pager(),
                'page_start': page_info.start,
            }
            # 加入全局变量
            ret['global_dict'] = {
                'contact_list': self.contact_list,
                'manager_list': self.manager_list
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def delete_business_unit(request):
        """
        删除业务线
        :param request:
        :return:
        """
        response = BaseResponse()
        try:
            id_list = request.POST.getlist('id_list')
            models.BusinessUnit.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def update_business_unit(request):
        """
        更新业务线
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
            form_obj = BusinessUnitUpdateJsonForm(row_dict)
            # 字段全部验证正确
            if form_obj.is_valid():
                models.BusinessUnit.objects.filter(id=nid).update(**form_obj.cleaned_data)
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
                    models.BusinessUnit.objects.filter(id=nid).update(**row_dict)
                else:
                    response.status = False
                    error_count += 1
        if error_count:
            response.message = '共%s条,失败%s条' % (len(update_list), error_count)
        else:
            response.message = '更新成功'
        return response
