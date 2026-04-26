# system/user

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class UserPage(BasePage):
    """登录页面"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.navigate_to('system/user')

    def search_user(self, name):
        self.input_by_css('input[placeholder=请输入用户名称]', name)
        self.click_ele_by_role('button', '搜索')

    def add_user(self, name, email, password):
        self.click_ele_by_role('button', '新建用户')
        self.input_by_css('.n-form input[placeholder=请输入用户名称]', name)
        self.input_by_css('.n-form input[placeholder=请输入邮箱]', email)
        self.input_by_css('.n-form input[placeholder=请输入密码]', password)
        self.input_by_css('.n-form input[placeholder=请确认密码]', password)
        self.click_ele_by_role('checkbox', '普通用户')
        self.click_ele_by_role('button', '保存')
        self.assert_ele_visible_by_txt('新增成功')

    def del_user(self, name):
        self.search_user(name)
        self.sleep(100)
        self.click_ele_by_role('button', '删除')
        self.click_ele_by_role('button', '确认')
        self.assert_ele_visible_by_txt('删除成功')
        
    def del_user_faild(self, name):
        self.search_user(name)
        self.sleep(100)
        self.click_ele_by_role('button', '删除')
        self.click_ele_by_role('button', '确认')
        self.assert_ele_visible_by_txt('删除失败')
