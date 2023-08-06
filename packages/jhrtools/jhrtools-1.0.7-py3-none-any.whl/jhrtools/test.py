#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/3/9 14:23
@Author   : ji hao ran
@File     : test.py
@Project  : pkgDev
@Software : PyCharm
"""
import json
import requests
from jhrtools import RTDBPointTable, RuleMatch, Mysql

if __name__ == '__main__':
    print(Mysql().read(table_names='tb_tenant'))

    r = RuleMatch(tenant_id='SHZRBWG',
                  project_id='SHZRBWG',
                  rb=json.loads(requests.get('http://192.168.1.97:9991/static/data/api.json').text),
                  pt=RTDBPointTable().point_table)
    print(r.available_rules)

    df = RTDBPointTable(project_name=['jet_101_shzg_dev', 'jet_101_lghb_dev']).point_table
    print(df.head())
