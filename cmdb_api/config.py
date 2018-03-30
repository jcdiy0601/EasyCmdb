#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

PLUGINS_AGENT_DICT = {
    'basic': 'cmdb_api.service.agent.basic.HandleBasic',
    'nic': 'cmdb_api.service.agent.nic.HandleNic',
    'memory': 'cmdb_api.service.agent.memory.HandleMemory',
    'disk': 'cmdb_api.service.agent.disk.HandleDisk'
}

PLUGINS_SNMP_DICT = {
    'server': {
        'basic': 'cmdb_api.service.snmp.server.basic.HandleBasic',
        'nic': 'cmdb_api.service.snmp.server.nic.HandleNic',
        'memory': 'cmdb_api.service.snmp.server.memory.HandleMemory',
        'disk': 'cmdb_api.service.snmp.server.disk.HandleDisk'
    },
    'switch': {
        'basic': 'cmdb_api.service.snmp.switch.basic.HandleBasic',
    },
    'firewall': {
        'basic': 'cmdb_api.service.snmp.firewall.basic.HandleBasic',
    }
}
