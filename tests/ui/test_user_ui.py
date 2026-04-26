import pytest
import allure
from playwright.sync_api import Page

from src.pages.user import UserPage
from settings import env, ACCOUNT
from src.pages.login import LoginPage


@pytest.fixture()
def login_page(page: Page):
    """登录 LoginPage"""
    login_page = LoginPage(page, env.base_url, **ACCOUNT.admin)
    yield login_page


@pytest.fixture()
def user_page(page: Page):
    """返回 UserPage"""
    yield UserPage(page)


@allure.feature("系统管理")
@allure.story("用户管理")
class TestUser:

    @allure.title("添加和删除用户")
    @allure.description("测试添加和删除用户数据")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_user(self, login_page: LoginPage, user_page: UserPage):
        name = 'UI 自动化测试'
        with allure.step("添加用户"):
            user_page.add_user(name, '16108045@qq.com', '12345')

        with allure.step("删除用户"):
            user_page.del_user(name)

        with allure.step("执行db删除除了 admin 以外的 user"):
            user_page.add_user('需要执行 db 删除的 user', '16108046@qq.com', '12345')
            login_page.client.db.fastapi_admin.delete("user", "username='需要执行 db 删除的 user'")

    @allure.title("删除不存在的用户")
    @allure.description("失败用例查看报告的截图和视频")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_delete_non_existent_users(self, login_page: LoginPage, user_page: UserPage):
        with allure.step("删除不存在的用户"):
            user_page.add_user('UI 自动化测试', '16108045@qq.com', '12345')
            user_page.del_user_faild('UI 自动化测试')
