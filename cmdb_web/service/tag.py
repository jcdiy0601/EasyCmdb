#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from utils.response import BaseResponse
from cmdb_data import models
from cmdb_web.service.base import BaseServiceList
from utils.pager import PageInfo
import json
from cmdb_web.forms.tag_form import TagUpdateJsonForm


class Tag(BaseServiceList):
    def __init__(self):
        # 查询条件配置
        condition_config = [
            {'name': 'name', 'text': '标签名称', 'condition_type': 'input'},
        ]
        # 表格配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段
                'title': 'ID',  # 前端表格中显示的字段
                'display': 0,  # 是否在前端显示，0为不显示，1为显示
                'text': {'content': '{n}', 'kwargs': {'n': '@id'}},  # 显示内容，字符串表示直接引用，@表示去数据库查询，@@表示特殊处理
                'attr': {}  # 自定义属性
            },
            {
                'q': 'name',
                'title': '标签名称',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@name'}},
                'attr': {
                    'name': 'name',
                    'edit-enable': 'true',
                    'edit-type': 'input',
                    'origin': '@name'
                }
            },
        ]
        extra_select = {}
        super(Tag, self).__init__(condition_config, table_config, extra_select)

    def fetch_tag(self, request):
        """
        获取标签信息
        :param request:
        :return:
        """
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            tag_count = models.Tag.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), tag_count)
            tag_list = models.Tag.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list).order_by('id')[page_info.start:page_info.end]
            # 加入查询条件
            ret['condition_config'] = self.condition_config
            # 加入配置文件
            ret['table_config'] = self.table_config
            # 加入查询到的数据
            ret['data_list'] = list(tag_list)
            # 加入页面信息
            ret['page_info'] = {
                'page_str': page_info.pager(),
                'page_start': page_info.start,
            }
            # 加入全局变量
            ret['global_dict'] = {}
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def delete_tag(request):
        """
        删除标签
        :param request:
        :return:
        """
        response = BaseResponse()
        try:
            id_list = request.POST.getlist('id_list')
            models.Tag.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def update_tag(request):
        """
        更新标签
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
            form_obj = TagUpdateJsonForm(row_dict)
            # 字段全部验证正确
            if form_obj.is_valid():
                models.Tag.objects.filter(id=nid).update(**form_obj.cleaned_data)
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
                if '__all__' in json.loads(form_obj.errors.as_json()):
                    message = json.loads(form_obj.errors.as_json())['__all__'][0]['message']
                    flag_tag = True
                response.error.append({'num': num, 'message': message})
                if not flag_tag:
                    models.Tag.objects.filter(id=nid).update(**row_dict)
                else:
                    response.status = False
                    error_count += 1
        if error_count:
            response.message = '共%s条,失败%s条' % (len(update_list), error_count)
        else:
            response.message = '更新成功'
        return response
