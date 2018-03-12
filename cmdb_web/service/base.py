#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import json
from django.db.models import Q


class BaseServiceList(object):
    def __init__(self, condition_config, table_config, extra_select):
        """
        :param condition_config: 查询条件配置
        :param table_config: 表格配置
        {
            'q': 'title',       # 用于数据库查询的字段，即Model.Tb.objects.xxx.values(*['v',]), None则表示不获取相应的数据库列
            'title': '标题',     # table表格显示的列名
            'display': 0        # 实现在表格中显示 0，不显示；1显示
            'text': {'content': "{id}", 'kwargs': {'id': '@id'}}, # 表格的每一个td中显示的内容,一个@表示获取数据库查询字段，两个@@，表示根据当前id在全局变量中找到id对应的内容
            'attr': {}          # 自定义属性
        }
        :param extra_select: 额外配置
        """
        self.condition_config = condition_config
        self.table_config = table_config
        self.extra_select = extra_select

    @property
    def values_list(self):
        """
        数据库查询时的指定字段
        :return:
        """
        values = []
        for item in self.table_config:
            if item['q']:
                values.append(item['q'])
        return values

    @staticmethod
    def select_condition(request):
        """
        获取前端通过ajax发过来的查询条件，前端发过来的是字符串，这里要转成字典
        :param request:
        :return:
        """
        # 获取前端通过ajax发送过来的查询条件
        con_str = request.GET.get('condition', None)
        if not con_str:
            con_dict = {}
        else:
            # 前端发送过来的是字符串，这里要将字符串转成字典
            con_dict = json.loads(con_str)
        con_q = Q()
        for k, v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con_q.add(temp, 'AND')
        return con_q
