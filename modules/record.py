"""
    @Author: ImYrS Yang
    @Date: 2022/6/17
    @Copyright: ImYrS Yang
    @Description: 
"""

import logging as log
from typing import Optional

import requests

from modules import auth


def get_zone_id(name: str) -> Optional[str]:
    """
    使用 zone 查询 zone_id
    :param name: 域名
    :return: 请求成功返回 zone_id, 失败返回 None
    """
    try:
        resp = requests.get(
            'https://dns.cn-south-1.myhuaweicloud.com/v2/zones',
            headers={'X-Auth-Token': auth.get().token},
            params={'name': name},
        )

        resp.raise_for_status()

        data = resp.json()
        for i in data['zones']:
            if i['name'] == name:
                return i['id']

        log.error(f'[Record] 未能查询到 zone_id: {data}')
        return None
    except requests.RequestException as e:
        log.error(f'[Record] 查询 zone_id 失败: {e}')
        return None


def update_record(zone_id: str, name: str, ip: str) -> Optional[bool | dict | str]:
    """
    更新 DNS 记录

    先使用 name 查询 record_id, 未查询到则直接创建记录

    :param zone_id: 域名 zone_id
    :param name: 记录值, 完整域名
    :param ip: 记录值, IP 地址
    :return:
    """
    try:
        resp = requests.get(
            f'https://dns.cn-south-1.myhuaweicloud.com/v2/zones/{zone_id}/recordsets',
            headers={'X-Auth-Token': auth.get().token},
            params={'name': name},
        )

        resp.raise_for_status()

        data = resp.json()
        record_id = None
        for i in data['recordsets']:
            if i['name'] == name:
                record_id = i['id']
                if i['records'][0] == ip:
                    return '域名解析记录未变化'
                break

        return create(
            zone_id=zone_id, name=name, record=ip
        ) if not record_id else update(
            zone_id=zone_id, record_id=record_id, name=name, record=ip
        )
    except requests.RequestException as e:
        log.error(f'[Record] 查询 record_id 失败: {e}')
        return None


def update(
        zone_id: str,
        record_id: str,
        name: str,
        record: Optional[str] = None,
        records: Optional[list[str]] = None,
        record_type: Optional[str] = 'A',
        ttl: Optional[int] = 60,
) -> Optional[bool | dict]:
    """
    更新 DNS 记录
    :param zone_id: 域名 zone_id
    :param record_id: 记录 id
    :param name: 完整域名
    :param record: 记录值, 如果 records 不为 None, 则忽略 record
    :param records: 记录值列表
    :param record_type: 记录类型
    :param ttl: 过期时间
    :return: 请求成功返回 True, 失败返回 dict, 发生错误返回 None
    """
    try:
        resp = requests.put(
            f'https://dns.cn-south-1.myhuaweicloud.com/v2/zones/{zone_id}/recordsets/{record_id}',
            headers={'X-Auth-Token': auth.get().token},
            json={
                'name': name,
                'type': record_type,
                'ttl': ttl,
                'records': records or [record]
            },
        )

        if 200 <= resp.status_code < 300:
            return True
        else:
            return resp.json()
    except requests.RequestException as e:
        log.error(f'[Record] 更新记录失败: {e}')
        return None


def create(
        zone_id: str,
        name: str,
        record: Optional[str] = None,
        records: Optional[list[str]] = None,
        record_type: Optional[str] = 'A',
        ttl: Optional[int] = 60,
) -> Optional[bool | dict]:
    """
    创建 DNS 记录
    :param zone_id: 域名 zone_id
    :param name: 完整域名
    :param record: 记录值, 如果 records 不为 None, 则忽略 record
    :param records: 记录值列表
    :param record_type: 记录类型
    :param ttl: 过期时间
    :return: 请求成功返回 True, 失败返回 dict, 发生错误返回 None
    """
    try:
        resp = requests.post(
            f'https://dns.cn-south-1.myhuaweicloud.com/v2/zones/{zone_id}/recordsets',
            headers={'X-Auth-Token': auth.get().token},
            json={
                'name': name,
                'type': record_type,
                'ttl': ttl,
                'records': records or [record]
            },
        )

        if 200 <= resp.status_code < 300:
            return True
        else:
            return resp.json()
    except requests.RequestException as e:
        log.error(f'[Record] 创建记录失败: {e}')
        return None
