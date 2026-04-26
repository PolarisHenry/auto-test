# user_per.py
import os
from locust import HttpUser, task, between
from faker import Faker
from src.core.http_client import HttpClient
from settings import ACCOUNT, ENV

fake = Faker('zh_CN')


# 定义用户行为
class UserPer(HttpUser):
    host = ENV.test.strip('/')
    # 每次请求之间的等待时间 (1~3 秒随机)
    wait_time = between(1, 3)

    def on_start(self):
        # 初始化 HttpClient 进行登录并获取 Token
        self.cl = HttpClient()
        self.cl.session = self.client
        self.cl.login(self.host, **ACCOUNT.admin)

    # 定义一个测试任务
    @task
    def add_and_del_user(self):
        # 创建用户
        username = fake.name()
        email = fake.email()
        res = self.cl.api_v1_user_create_p(
            username=username, password='123456', is_active=1, email=email
        )
        
        # 检查创建是否成功
        if res.status_code != 200:
            raise Exception(f"创建用户失败: {res.text}")
        
        # 查询用户ID
        res = self.cl.api_v1_user_list_g(username=username)
        user_id = res.search('data[0].id')
        
        if not user_id:
            raise Exception(f"未找到用户: {username}")
        
        # 删除用户
        delete_res = self.cl.api_v1_user_delete_del(user_id)
        
        # 检查删除是否成功
        if delete_res.status_code != 200:
            raise Exception(f"删除用户失败: {delete_res.text}")


if __name__ == '__main__':
    os.system('locust -f user_per.py')
