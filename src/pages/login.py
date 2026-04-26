import json
import time
from urllib.parse import urljoin, urlparse

from playwright.sync_api import Page

from src.core.http_client import HttpClient
from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """登录页面

    Args:
        page (Page): playwright 的 page 
        base_url (Page): 基础网址
        username (Page): 账号
        password (Page): 密码
    """

    def __init__(self, page: Page, base_url: str, username: str, password: str):
        super().__init__(page)
        url = urljoin(base_url, 'login')
        self.navigate_to(url)
        self.client = HttpClient(base_url, username, password)
        
        # 设置cookie
        if self.client.session.cookies:
            cookies_to_add = []
            for cookie in self.client.session.cookies:
                cookie_dict = {
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': (
                        cookie.domain if cookie.domain else urlparse(base_url).hostname
                    ),
                    'path': cookie.path if cookie.path else '/',
                    'httpOnly': False,  # 根据实际情况调整
                    'secure': (cookie.secure if hasattr(cookie, 'secure') else True),
                }
                # 只在 expires 有效时设置（应为数字时间戳）
                if cookie.expires is not None and isinstance(
                    cookie.expires, (int, float)
                ):
                    cookie_dict['expires'] = cookie.expires
                cookies_to_add.append(cookie_dict)
                self.page.context.add_cookies(cookies_to_add)

        # 设置Localstorage 的token
        if self.client.session.headers['Token']:
            token_value = self.client.session.headers['Token']
            # 获取当前时间戳（毫秒）
            current_timestamp_ms = int(time.time() * 1000)
            # 构造要存储到 local storage 的 JSON 对象
            local_storage_data = {
                "value": token_value,
                "time": current_timestamp_ms,
                "expire": None,  # 根据需求设置过期时间，这里设置为 None
            }
            # 将 JSON 对象转换为字符串
            local_storage_json_string = json.dumps(local_storage_data)
            # 使用 Playwright 的 evaluate 方法将数据存储到浏览器的 local storage 中
            self.page.evaluate(
                f"localStorage.setItem('ACCESS_TOKEN', '{local_storage_json_string}')"
            )
