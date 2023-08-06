#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/3/9 14:23
@Author   : ji hao ran
@File     : test.py
@Project  : pkgDev
@Software : PyCharm
"""

from jhrtools import *

if __name__ == '__main__':
    print(Mysql().read(table_names='tb_tenant'))

    r = RuleMatch(tenant_id='SHZRBWG',
                  project_id='SHZRBWG',
                  rb=Rule().rb,
                  pt=RTDBPointTable().pt)
    print(r.available_rules)

    df = RTDBPointTable(project_name=['jet_101_shzg_dev', 'jet_101_lghb_dev']).pt
    print(df.head())

    Kafka().produce(1)
