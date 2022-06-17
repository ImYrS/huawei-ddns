"""
    @Author: ImYrS Yang
    @Date: 2022/6/17
    @Copyright: ImYrS Yang
    @Description: 
"""

import os

import config
from modules import ip, record
from modules.database import db, Token

os.environ['NO_PROXY'] = '*'


def main():
    """主函数"""
    print(f'\n\033[1;37;41m Huawei Cloud DDNS \033[1;30;47m By ImYrS \033[0m\n')

    zone = config.zone

    if not zone.endswith('.'):
        zone += '.'  # 域名必须以 '.' 结尾

    full_name = f'{config.record}.{zone}'
    print(f'域名: {full_name}')

    print('正在获取 IP 地址')
    current_ip = ip.get()

    if current_ip is None:
        raise Exception('获取 IP 地址失败')

    print(f'当前 IP: {current_ip}')
    print(f'正在查询解析记录')

    zone_id = record.get_zone_id(zone)
    if zone_id is None:
        raise Exception('获取 zone_id 失败')
    print(f'zoneId: {zone_id}')

    result = record.update_record(zone_id, full_name, current_ip)
    if result is not True:
        if isinstance(result, str):
            print(result)
        elif isinstance(result, dict):
            raise Exception(f'更新记录失败, 响应: {result}')
        else:
            Exception('更新记录失败')

    else:
        print(f'更新成功')


def init():
    """初始化"""
    init_db()
    main()


def init_db():
    """初始化数据库"""
    if not os.path.exists(config.db_name):
        db.create_tables([Token])


if __name__ == '__main__':
    init()
