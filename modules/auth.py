"""
    @Author: ImYrS Yang
    @Date: 2022/6/17
    @Copyright: ImYrS Yang
    @Description: 
"""

import logging as log
from typing import Optional

import requests
import peewee

import config
from modules import common
from modules.database import Token


def get() -> Optional[Token]:
    """
    获取华为云 Token
    :return: 请求成功返回 Token 对象, 失败返回 None
    """
    try:
        token = Token.select().order_by(Token.id.desc()).get()

        # 判断 Token 是否过期
        if token.created_at + 60 * 60 * 23 * 1000 < common.now():
            return refresh()
        else:
            return token
    except peewee.DoesNotExist:
        return refresh()
    except peewee.PeeweeException as e:
        log.error(f'[Auth] 获取 token 失败: {e}')
        return None


def refresh() -> Optional[Token]:
    """
    刷新华为云 Token
    :return: 请求成功返回 Token 对象, 失败返回 None
    """
    try:
        resp = requests.post(
            'https://iam.myhuaweicloud.com/v3/auth/tokens',
            json={
                'auth': {
                    'identity': {
                        'methods': ['password'],
                        'password': {
                            'user': {
                                'domain': {
                                    'name': config.domain_name
                                },
                                'name': config.username,
                                'password': config.password
                            },
                        }
                    },
                    'scope': {
                        'domain': {
                            'name': config.domain_name
                        }
                    }
                }
            },
        )

        resp.raise_for_status()

        token = resp.headers['X-Subject-Token']

        return Token.create(
            token=token,
            created_at=common.now(),
        )
    except requests.RequestException as e:
        log.error(f'[Auth] 获取 token 失败: {e}')
        return None
