#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

PLUGINS_DICT = {
    'basic': 'cmdb_api.service.asset.HandleBasic',
    'nic': 'cmdb_api.service.asset.HandleNic',
    'memory': 'cmdb_api.service.asset.HandleMemory',
    'disk': 'cmdb_api.service.asset.HandleDisk'
}