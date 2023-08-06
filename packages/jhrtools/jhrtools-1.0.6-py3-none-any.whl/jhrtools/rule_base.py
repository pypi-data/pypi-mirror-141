#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2022/3/9 13:34
@Author   : ji hao ran
@File     : rule_base.py
@Project  : pkgDev
@Software : PyCharm
"""
import json
import re
import pandas as pd
from typing import List
from itertools import product
from rtdb import RTDBPointTable
import requests


class RuleMatch:

    def __init__(self, tenant_id: str, project_id: str, rb: dict, pt: pd.DataFrame):
        """

        :param tenant_id: 项目集团id
        :param project_id: 项目id
        :param rb: 规则库
        :param pt: 点位表
        """
        self.tenant_id = tenant_id
        self.project_id = project_id
        self.rb = rb
        self.pt = pt

    @property
    def _project_pt(self):
        """项目目标点位表"""
        return self.pt.query(f'tenant_id=="{self.tenant_id}" and project_id=="{self.project_id}"')

    @staticmethod
    def _judge_point_id(table, point_id: List[str]):
        # 含有通配符的point_id
        glob_point_id = [i for i in point_id if '*' in i]
        # 不含通配符的point_id
        normal_point_id = [i for i in point_id if '*' not in i]
        # 判断表含正常的point_id
        normal_judge = set(normal_point_id).issubset(set(table['point_id']))
        # 判断统配point_id
        glob_judge = True
        if glob_point_id:
            result = []
            for i in glob_point_id:
                pattern = i.replace('*', '_\\d+')  # 匹配point_id系列
                find = re.findall(pattern, ''.join(table['point_id']))
                result.append(len(find) > 0)
            if not all(result):
                glob_judge = False
        return True if normal_judge and glob_judge else False

    def _find_equip(self, table: pd.DataFrame, rule_equip: dict):
        """查找具体设备

        :param table: 点位表
        :param rule_equip: 规则的rule_equip中的一个元素
        :return: 查找的具体设备
        :rtype: dict
        """

        type_ = rule_equip.get('type')
        template = rule_equip.get('template')
        point_id = rule_equip.get('point_id')
        result = []
        if template is None:  # 没有模板
            df = table.query(f'equip_type=="{type_}"')
        else:
            df = table.query(f'equip_type=="{type_}" and template_id=="{template}"')
        if not df.empty:
            result = []
            for g, g_df in df.groupby('equip_id'):
                if self._judge_point_id(g_df, point_id):
                    result.append(g)
        return {'type': type_, 'template': template, 'equip_id': result}

    def find_equips(self, rule: dict):
        """查找项目所有满足规则的设备

        :param rule: 单个规则
        """
        result = []
        obj = rule.get('rule_obj').get('type')
        obj_all = rule.get('rule_obj').get('use_all')
        # 点位表
        sys_df = self._project_pt[self._project_pt['equip_sys_type_id'] == obj]
        if not sys_df.empty:
            gb = sys_df.groupby('equip_sys_id')
            if not obj_all:
                for label, df in gb:  # 遍历系统id
                    equips = [self._find_equip(df, i) for i in rule.get('rule_equip')]
                    all_exist = all([i.get('equip_id') for i in equips])
                    if all_exist:
                        result.append({'equip_sys_id': label, 'rule_equip': equips})
            else:
                equips = [self._find_equip(sys_df, i) for i in rule.get('rule_equip')]
                all_exist = all([i.get('equip_id') for i in equips])
                if all_exist:
                    result.append({'equip_sys_id': obj, 'rule_equip': equips})
        return result

    @property
    def available_rules(self):
        """根据集团，项目匹配能够应用的规则
        """

        obj_rule = []
        for k, v in self.rb.items():  # 遍历所有规则
            result = self.find_equips(v)
            if result:
                obj_rule.append(k)
        return obj_rule

    def _create_job_conf(self, rule: dict, sys_equip: dict):
        """创建任务的配置文件

        :param rule: 某个规则
        :param sys_equip: 某个系统下的匹配设备
        :return: 批量匹配的规则任务配置
        :rtype: dict
        """
        equip_sys_id = sys_equip.get('equip_sys_id')
        equip = sys_equip.get('rule_equip')
        task_id_prefix = f'{rule.get("rule_url")}_{self.tenant_id}_{self.project_id}_{equip_sys_id}'
        task = rule.copy()
        task.update({'tenant_id': self.tenant_id, 'project_id': self.project_id, 'equip_sys_id': equip_sys_id})
        # 添加具体设备
        for i, v in enumerate(task.get('rule_equip')):
            task.get('rule_equip')[i].update(equip[i])
        # 需要排列的设备索引
        prod_idx = [i for i, v in enumerate(task.get('rule_equip')) if not v.get('use_all')]
        if not prod_idx:  # 不存在需要排列的设备
            task_id = f'{task_id_prefix}_1'
            task.update({'task_id': task_id})
            return {task_id: task}
        # 设备全排列
        all_prod = list(product(*[task.get("rule_equip")[i].get('equip_id') for i in prod_idx]))
        result = {}
        for i, prod_value in enumerate(all_prod):  # 遍历所有组合
            task_id = f'{task_id_prefix}_{i}'
            task.update({'task_id': task_id})
            for j, value in enumerate(prod_idx):  # 更新equip_id
                task.get('rule_equip')[value].update({'equip_id': prod_value[j]})
            result.update({task_id: json.loads(json.dumps(task))})
        return result

    def build_tasks(self, rule: dict):
        """批量建立规则的任务配置

        :param rule: 规则
        """
        result = {}
        for sys_equip in self.find_equips(rule):
            d = self._create_job_conf(rule, sys_equip)
            result.update(d)
        return result


if __name__ == '__main__':
    r = RuleMatch(tenant_id='SHZRBWG',
                  project_id='SHZRBWG',
                  rb=json.loads(requests.get('http://192.168.1.97:9991/static/data/api.json').text),
                  pt=RTDBPointTable().point_table)
    print(r.available_rules)
