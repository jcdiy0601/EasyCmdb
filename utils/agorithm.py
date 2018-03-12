#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen


def get_intersection(*args):
    """
    获取所有set的并集
    :param args:
    :return:
    """
    base = args[0]
    result = base.intersection(*args)
    return list(result)


def get_exclude(total, part):
    result = []
    for item in total:
        if item in part:
            pass
        else:
            result.append(item)
    return result
