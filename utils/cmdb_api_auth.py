#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

import time
import hashlib
from django.http import JsonResponse
from django.conf import settings

ENCRYPT_LIST = [
    # {'encrypt': encrypt, 'time': timestamp}
]


def cmdb_api_auth_method(request):
    auth_key = request.META.get(settings.ASSET_AUTH_HEADER_NAME)  # f73c8691e6c932f2063652796cb49186|1512458859.455036
    if not auth_key:
        return False
    sp = auth_key.split('|')
    if len(sp) != 2:
        return False
    encrypt, timestamp = sp     # encrypt='f73c8691e6c932f2063652796cb49186' timestamp='1512458859.455036'
    timestamp = float(timestamp)    # timestamp=1512458859.455036
    limit_timestamp = time.time() - settings.ASSET_AUTH_TIME    # 当前时间减2秒
    if limit_timestamp > timestamp:     # 超时，超时时间2秒
        return False
    ha = hashlib.md5(settings.ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes('%s|%f' % (settings.ASSET_AUTH_KEY, timestamp), encoding='utf-8'))
    result = ha.hexdigest()
    if encrypt != result:  # 认证失败
        return False
    exist = False
    del_keys = []
    for k, v in enumerate(ENCRYPT_LIST):
        m = v['time']
        n = v['encrypt']
        if m < limit_timestamp:     # 之前记录的时间小于最大超时时间
            del_keys.append(k)
            continue
        if n == encrypt:          # 新的加密内容|前面部分与之前记录相同
            exist = True
    del_keys = sorted(del_keys, reverse=True)
    for k in del_keys:
        del ENCRYPT_LIST[k]
    if exist:
        return False
    ENCRYPT_LIST.append({'encrypt': encrypt, 'time': timestamp})
    return True


def cmdb_api_auth(func):
    """
    API验证装饰器
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if not cmdb_api_auth_method(request):
            return JsonResponse({'code': 401, 'message': 'API认证失败'}, json_dumps_params={'ensure_ascii': False})
        return func(request, *args, **kwargs)
    return wrapper
