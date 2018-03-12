#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen


def ip_sort(available_ip_list):
    """
    ip排序（快排算法）
    :param available_ip_list:
    :return:
    """
    for i in range(len(available_ip_list)-1):
        for j in range(len(available_ip_list)-i-1):
            if int(available_ip_list[j].split('.')[-1]) > int(available_ip_list[j+1].split('.')[-1]):
                available_ip_list[j], available_ip_list[j + 1] = available_ip_list[j + 1], available_ip_list[j]
    return available_ip_list
