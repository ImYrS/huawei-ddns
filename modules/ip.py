"""
    @Author: ImYrS Yang
    @Date: 2022/6/17
    @Copyright: ImYrS Yang
    @Description: 
"""

import logging as log
from typing import Optional

import requests


def get() -> Optional[str]:
    """
    获取当前 IP 地址
    """
    try:
        resp = requests.get('https://httpbin.org/get')
        resp.raise_for_status()
        data = resp.json()
        return data['origin']
    except requests.RequestException as e:
        log.error(f'[IP] 获取 IP 失败: {e}')
        return None
