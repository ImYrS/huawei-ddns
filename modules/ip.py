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
        response = requests.get('https://ip.42.pl/text')
        return response.text
    except requests.RequestException as e:
        log.error(f'[IP] 获取 IP 失败: {e}')
        return None
