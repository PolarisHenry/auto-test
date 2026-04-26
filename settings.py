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
    # 各环境域名配置（本地开发按需修改地址）
    test = 'http://192.168.1.19:3100'
    online = 'http://192.168.1.19:3100'

    # 当前目标环境：本地改这里切换环境，Jenkins 通过 TARGET_ENV 环境变量注入
    _target = os.environ.get('TARGET_ENV', 'test')

    @property
    def base_url(self):
        """返回当前目标环境的域名（Jenkins 通过 BASE_URL 环境变量可覆盖）"""
        default = getattr(self, self._target)
        return os.environ.get('BASE_URL', default)


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


# Allure 报告地址（仅在 Jenkins 环境中自动获取，本地运行时为 None）
_JENKINS_URL = os.environ.get('JENKINS_URL', '')
_JOB_NAME = os.environ.get('JOB_NAME', '')
ALLURE_REPORT_URL = f"{_JENKINS_URL}job/{_JOB_NAME}/allure/" if _JENKINS_URL and _JOB_NAME else None


env = ENV()
account = ACCOUNT()

if __name__ == '__main__':
    print(DB.fastapi_admin)
