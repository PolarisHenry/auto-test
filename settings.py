import os
from pathlib import Path

from src.core.db_client import MysqlClient

# 项目根路径：请使用正斜杠进行路径拼接。示例：testcase_dir = ROOT_DIT / 'tests'
ROOT_PATH = Path(__file__).parent

API_DB_PATH = ROOT_PATH / 'src/core/data/apis.db'
OPENPAI_PATH =  ROOT_PATH / 'src/core/openapi'
OPENPAI_URLS = {
        'openapi': 'http://localhost:3100/openapi.json',
        # 可以有多个 openapi 文档
    }

# 企业微信机器人 Webhook（可被环境变量 WECOM_WEBHOOK 覆盖）
WECOM_WEBHOOK: str = os.environ.get(
    'WECOM_WEBHOOK',
    'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=22c77179-cd50-415c-9fb2-8592ef01e866'
)

class ENV:
    # 测试
    # test = os.environ.get('BASE_URL', 'http://localhost:3100')
    test = 'http://192.168.1.19:3100'

    # 线上
    # online = os.environ.get('BASE_URL', 'http://localhost:3100')


class ACCOUNT:
    admin = {'username': 'admin', 'password': '123456'}


class DB:
    """
    调用示例：
    self.db.amz_up.query(sql)
    self.db.data.execute(sql)
    """

    __COMMON_DB_CONFIG = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', '3306')),
        'user': os.environ.get('DB_USER', 'fastapi_admin'),
        'password': os.environ.get('DB_PASSWORD', 'fastapi_admin_password'),
        'charset': "utf8",
    }

    fastapi_admin: dict | MysqlClient = {
        **__COMMON_DB_CONFIG,
        'database': os.environ.get('DB_NAME', 'fastapi_admin'),
    }


env = ENV()
account = ACCOUNT()

if __name__ == '__main__':
    print(DB.fastapi_admin)
