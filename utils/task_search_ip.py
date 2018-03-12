#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: JiaChen

from concurrent.futures import ThreadPoolExecutor
import subprocess


class SearchIp(object):
    """
    查询可用IP类，多线程执行
    """
    def __init__(self, ip_list):
        self.ip_list = ip_list
        self.available_ip_list = []

    def process(self):
        pool = ThreadPoolExecutor(20)  # 线程池启动20个线程
        for ip in self.ip_list[2:-2]:
            pool.submit(self.run, ip)
        pool.shutdown(wait=True)
        return self.available_ip_list

    def run(self, ip):
        res = subprocess.call('ping %s' % ip, shell=True)
        # res = subprocess.call('ping %s -c 1 > /dev/null' % ip, shell=True)
        if res:
            self.available_ip_list.append(str(ip))
