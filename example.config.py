"""
    @Author: ImYrS Yang
    @Date: 2022/6/17
    @Copyright: ImYrS Yang
    @Description:
"""

"""
该程序授权方式基于华为云 IAM 用户.

需前往观礼台授予 IAM 用户相关权限, 并使用 IAM 账号和密码.
第三方系统用户可用性未知.
"""

username = ''  # IAM 账号
domain_name = ''  # IAM 所属账号名称
password = ''  # IAM 密码

"""
DDNS 域名为 ddns.example.com 时设定如下

zone = 'example.com'
record = 'ddns'

未添加的解析记录会尝试自动创建, 但可能遇到 "Authentication required. Invalid project ID in token." 错误. 可能是 IAM 用户权限问题.
"""

zone = 'example.cn'  # 主域名
record = 'ddns'  # 子域名, 可为空

"""数据库文件名"""
db_name = 'data.db'
