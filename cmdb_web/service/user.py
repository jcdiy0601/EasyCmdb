#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from utils.response import BaseResponse
from cmdb_data import models
from cmdb_web.service.base import BaseServiceList
from utils.pager import PageInfo


class User(BaseServiceList):
    def __init__(self):
        # 查询条件配置
        condition_config = [
            {'name': 'email', 'text': '邮箱', 'condition_type': 'input'},
            {'name': 'name', 'text': '姓名', 'condition_type': 'input'},
            {'name': 'phone', 'text': '电话', 'condition_type': 'input'},
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
                'q': 'email',
                'title': '邮箱',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@email'}},
                'attr': {}
            },
            {
                'q': 'name',
                'title': '姓名',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'phone',
                'title': '手机号',
                'display': 1,
                'text': {'content': '{n}', 'kwargs': {'n': '@phone'}},
                'attr': {}
            },
            {
                'q': None,
                'title': '选项',
                'display': 1,
                'text': {
                    'content': '<a href="/cmdb_web/user_edit_{n}.html" class="btn btn-xs btn-default">编辑</a> \
                    | <a href="/cmdb_web/user_change_pass_{n}.html" class="btn btn-xs btn-default">重置密码</a>\
                    | <a href="/cmdb_web/user_change_permission_{n}.html" class="btn btn-xs btn-default">修改权限</a>',
                    'kwargs': {'n': '@id'}
                },
                'attr': {}
            }
        ]
        extra_select = {}
        super(User, self).__init__(condition_config, table_config, extra_select)

    def fetch_user(self, request):
        """
        获取用户信息
        :param request:
        :return:
        """
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.select_condition(request)
            user_count = models.UserProfile.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), user_count)
            user_list = models.UserProfile.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list).order_by('id')[page_info.start:page_info.end]
            # 加入查询条件
            ret['condition_config'] = self.condition_config
            # 加入配置文件
            ret['table_config'] = self.table_config
            # 加入查询到的数据
            ret['data_list'] = list(user_list)
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
    def delete_user(request):
        """
        删除用户
        :param request:
        :return:
        """
        response = BaseResponse()
        try:
            id_list = request.POST.getlist('id_list')
            models.UserProfile.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response
