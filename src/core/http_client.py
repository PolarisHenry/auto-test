# http_clinet.py
from urllib.parse import urljoin

from faker import Faker
import requests
from loguru import logger

from src.core.http_response import CustomResponse
from settings import ACCOUNT, API_DB_PATH, ENV
from src.apis import AllApiMixin
from src.core.db_client import MysqlClient, SqliteClient


class CustomRequests(requests.Session):
    def __init__(self):
        super().__init__()

    def request(self, method, url, **kwargs):
        logger.info(f"请求方法: {method}, 请求URL: {url}, 请求参数: {kwargs}")
        response = super().request(method, url, **kwargs)
        logger.info(f"响应状态码: {response.status_code}, 响应内容: {response.text}")
        return response


class HttpClient(AllApiMixin):
    session = CustomRequests()

    def __init__(self, base_url=None, username=None, password=None):
        super().__init__()
        self.base_url = base_url
        self.username = username
        self.password = password
        self.sqlitDB = SqliteClient(API_DB_PATH)
        self.__init_databases()
        if base_url and username and password:
            self.login(base_url, username, password)

    def request(self, method, url, **kwargs):

        return CustomResponse(
            self.session.request(method, urljoin(self.base_url, url), **kwargs)
        )

    def __init_databases(self):

        # 延迟导入 settings，避免循环依赖
        try:
            from settings import DB
        except ImportError:
            logger.error("无法导入 DB 配置，请检查 settings.py")
            raise

        self.db = DB()  # 此时 DB 已可访问

        db_keys = [i for i in DB.__dict__.keys() if not i.startswith('_')]
        print(db_keys)
        for i in db_keys:
            config = DB.__dict__[i]
            # 检查 config 是否为字典（兼容旧代码）
            if isinstance(config, dict):
                self.db.__dict__[i] = MysqlClient(config)
            elif isinstance(config, MysqlClient):
                self.db.__dict__[i] = config
            else:
                logger.warning(f"无效的 DB 配置类型: {i}")

    def __get_env(self):
        # 判断环境
        env = 'test'
        if self.base_url:
            if 'test' in self.base_url:
                env = 'test'
            elif 'online' in self.base_url:
                env = 'online'
        return env

    def login(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.env = self.__get_env()
        cookie_result = self.sqlitDB.query(
            f"select cookie from account_cookies where env='{self.env}' and username='{self.username}'"
        )
        if cookie_result:
            cookie_cache = cookie_result[0].get('cookie')
            self.session.headers['Token'] = cookie_cache
            login_message = self.api_v1_base_userinfo_g().search('msg')
            if login_message == 'OK':
                logger.info(
                    f'登录状态：{login_message},请求头Token缓存可用，无需重新登录'
                )
            else:
                logger.error(
                    f'登录状态：{login_message},请求头Token缓存不可用，需重新登录'
                )
                self.__login_and_set_token()
        else:
            logger.error(f'数据库中无缓存请求头Token，需重新登录')
            self.__login_and_set_token()

    def __login_and_set_token(self):
        res = self.api_v1_base_access_token_p(
            username=self.username, password=self.password
        )
        login_status = res.search('msg')
        if login_status == 'OK':
            access_token = res.search('data.access_token')
            self.session.headers['Token'] = access_token
            logger.info(f'登录成功,设置Token进入数据库')
            self.sqlitDB.delete(
                table='account_cookies',
                condition='env="{}" and username="{}"'.format(self.env, self.username),
            )
            self.sqlitDB.insert(
                table='account_cookies',
                fields='env,username,cookie',
                data=(self.env, self.username, access_token),
            )

        else:
            logger.error(f'登录失败，失败原因:{login_status}')
            raise Exception(f'登录失败，失败原因：{login_status}')


if __name__ == '__main__':
    client = HttpClient(ENV.test, **ACCOUNT.admin)
    fake = Faker('zh_CN')

    username = fake.name()
    email = fake.email()
    res = client.api_v1_user_create_p(
        username=username, password='123456', is_active=1, email=email
    )
