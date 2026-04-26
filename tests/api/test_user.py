import pytest
import allure

from settings import env, ACCOUNT
from src.core.http_client import HttpClient


@allure.feature("系统管理")
@allure.story("用户管理")
class TestUser:

    def setup_class(self):
        self.client = HttpClient(env.base_url, **ACCOUNT.admin)

    @allure.title("添加删除用户")
    @allure.description("添加用户，断言添加成功，把添加的用户删除，断言删除成功")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_add_user(self):
        with allure.step("添加用户"):
            self.client = HttpClient(env.base_url, **ACCOUNT.admin)
            res = self.client.api_v1_user_create_p(
                username='ceshi', password='123456', is_active=1, email='test@qq.com'
            )
            assert res.search('msg') == 'Created Successfully'

            res = self.client.api_v1_user_list_g(username='ceshi')
            user_id = res.search('data[0].id')
            assert res.search('data[0].email') == 'test@qq.com'
            assert res.search('data[0].username') == 'ceshi'

        with allure.step("删除用户"):
            assert (
                self.client.api_v1_user_delete_del(user_id).search('msg')
                == 'Deleted Successfully'
            )
            
        with allure.step("查数据库"):
            self.client.db.fastapi_admin.query('select * from user limit 1;')

    