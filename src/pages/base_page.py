# -*- coding: utf-8 -*-

"""
UI测试基础页面类
"""

from urllib.parse import urljoin, urlparse
from loguru import logger
from playwright.sync_api import Locator, Page, expect


class BasePage:
    """
    UI 测试基础页面类，封装了常用的 Playwright 页面操作和断言。
    """

    def __init__(self, page: Page):
        """
        初始化基础页面类

        Args:
            page (Page): Playwright Page 对象

        """

        self.page = page
        self.timeout = 5000  # 默认超时时间，单位毫秒

    def get_base_url(self) -> str:
        """
        获取当前页面的 base URL。
        """
        return f"{urlparse(self.page.url).scheme}://{urlparse(self.page.url).netloc}"

    def navigate_to(self, url: str, timeout: int = None):
        """
        导航到指定的 URL。如果 URL 不是完整的 HTTP/HTTPS 地址，则会与当前 base URL 拼接。

        Args:
            url (str): 目标 URL。
            timeout (int, optional): 导航操作的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """

        if not url.startswith('http'):
            url = urljoin(self.get_base_url(), url)
            self.page.goto(url, timeout=timeout or self.timeout)
        else:
            self.page.goto(url, timeout=timeout or self.timeout)
        logger.info(f"导航到 URL: {url}")

    def wait_for_load(self):
        """
        等待页面加载完成，直到网络空闲（networkidle）状态。
        """
        self.page.wait_for_load_state("networkidle")

    def sleep(self, time=100):
        """
        页面等待
        """
        logger.info(f'页面等待{time}ms')
        self.page.wait_for_timeout(time)

    def wait_ele_by_css(self, selector: str, timeout: int = None):
        """
        等待由 CSS 选择器定位的元素在页面上可见。

        Args:
            selector (str): CSS 选择器字符串。
            timeout (int, optional): 等待元素可见的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """
        element = self.locator_by_css(selector)
        expect(element).to_be_visible(timeout=timeout or self.timeout)
        logger.info(f"等待元素可见: {selector}")

    def locator_by_css(self, selector: str) -> Locator:
        """
        通过 CSS 选择器获取元素定位器。

        Args:
            selector (str): CSS 选择器字符串。

        Returns:
            Locator: Playwright Locator 对象。
        """
        return self.page.locator(selector)

    def locator_by_role(self, role: str, name: str, **kwargs) -> Locator:
        """
        通过元素的 ARIA 角色和可访问名称获取元素定位器。

        Args:
            role (str): 元素的 ARIA 角色，例如 'button', 'textbox', 'dialog' 等。
            name (str): 元素的可见文本或可访问名称。
            **kwargs: 传递给 Playwright `page.get_by_role` 方法的其他参数。

        Returns:
            Locator: Playwright Locator 对象。
        """
        logger.info(f"通过 role='{role}' 和 name='{name}' 查找元素")
        return self.page.get_by_role(role=role, name=name, **kwargs)

    def click_ele_by_txt(self, txt: str, timeout: int = None):
        """
        通过元素的可见文本点击元素。

        Args:
            txt (str): 要点击的元素的可见文本内容。
            timeout (int, optional): 点击操作的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """
        element = self.page.get_by_text(txt)
        element.click(timeout=timeout or self.timeout)
        logger.info(f"点击文本为 '{txt}' 的元素")

    def click_ele_by_css(self, selector: str, timeout: int = None):
        """
        通过 CSS 选择器点击元素。

        Args:
            selector (str): CSS 选择器字符串。
            timeout (int, optional): 点击操作的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """
        element = self.locator_by_css(selector)
        element.click(timeout=timeout or self.timeout)
        logger.info(f"点击 CSS 选择器为 '{selector}' 的元素")

    def click_ele_by_role(self, role: str, name: str, timeout: int = None):
        """
        通过元素的 ARIA 角色和可访问名称点击元素。

        Args:
            role (str): 元素的 ARIA 角色。
            name (str): 元素的可见文本或可访问名称。
            timeout (int, optional): 点击操作的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """
        element = self.locator_by_role(role, name)
        element.click(timeout=timeout or self.timeout)
        logger.info(f"点击 role='{role}' 和 name='{name}' 的元素")

    def input_by_css(self, selector: str, text: str, timeout: int = None):
        """
        在由 CSS 选择器定位的输入框中输入文本。

        Args:
            selector (str): CSS 选择器字符串。
            text (str): 要输入的文本内容。
            timeout (int, optional): 输入操作的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """
        self.page.fill(selector, text, timeout=timeout or self.timeout)
        logger.info(f"在 CSS 选择器为 '{selector}' 的元素中输入文本: '{text}'")

    def input_by_placeholder(self, placeholder: str, text: str, timeout: int = None):
        """
        在具有指定占位符的输入框中输入文本。

        Args:
            placeholder (str): 输入框的占位符文本。
            text (str): 要输入的文本内容。
            timeout (int, optional): 输入操作的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """
        self.page.get_by_placeholder(placeholder).fill(
            text, timeout=timeout or self.timeout
        )
        logger.info(f"在占位符为 '{placeholder}' 的元素中输入文本: '{text}'")

    def input_by_role(self, role: str, name: str, text: str, timeout: int = None):
        """
        在由 ARIA 角色和可访问名称定位的输入框中输入文本。

        Args:
            role (str): 元素的 ARIA 角色。
            name (str): 元素的可见文本或可访问名称。
            text (str): 要输入的文本内容。
            timeout (int, optional): 输入操作的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """
        element = self.locator_by_role(role, name)
        element.fill(text, timeout=timeout or self.timeout)
        logger.info(f"在 role='{role}' 和 name='{name}' 的元素中输入文本: '{text}'")

    def get_text(self, selector: str) -> str:
        """
        获取由 CSS 选择器定位的元素的文本内容。

        Args:
            selector (str): CSS 选择器字符串。

        Returns:
            str: 元素的文本内容。
        """
        element = self.locator_by_css(selector)
        text = element.text_content(timeout=self.timeout)
        logger.info(f"获取 CSS 选择器为 '{selector}' 的元素文本: '{text}'")
        return text

    def assert_ele_visible_by_css(self, selector: str, timeout: int = None) -> bool:
        """
        断言由 CSS 选择器定位的元素在页面上可见。

        Args:
            selector (str): CSS 选择器字符串。
            timeout (int, optional): 断言的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。

        Returns:
            bool: 如果元素可见则返回 True，否则抛出异常。
        """
        try:
            element = self.locator_by_css(selector).first
            expect(element).to_be_visible(timeout=timeout or self.timeout)
            logger.info(f"断言：CSS 选择器为 '{selector}' 的元素可见")
            return True
        except Exception as e:
            error_msg = f"断言失败：CSS 选择器为 '{selector}' 的元素不可见，原因： {e}"
            logger.error(error_msg)
            raise AssertionError(error_msg)

    def assert_ele_visible_by_role(
        self, role: str, name: str, timeout: int = None
    ) -> bool:
        """
        断言由 ARIA 角色和可访问名称定位的元素在页面上可见。

        Args:
            role (str): 元素的 ARIA 角色。
            name (str): 元素的可见文本或可访问名称。
            timeout (int, optional): 断言的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。

        Returns:
            bool: 如果元素可见则返回 True，否则抛出异常。
        """
        try:
            element = self.locator_by_role(role, name)
            expect(element).to_be_visible(timeout=timeout or self.timeout)
            logger.info(f"断言：role='{role}' 和 name='{name}' 的元素可见")
            return True
        except Exception as e:
            error_msg = f"断言失败：role='{role}' 和 name='{name}' 的元素不可见，原因： {e}"
            logger.error(error_msg)
            raise AssertionError(error_msg)

    def assert_ele_visible_by_txt(self, txt: str, timeout: int = None) -> bool:
        """
        断言具有指定文本内容的元素在页面上可见。

        Args:
            txt (str): 元素的可见文本内容。
            timeout (int, optional): 断言的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。

        Returns:
            bool: 如果元素可见则返回 True，否则抛出异常。
        """
        try:
            element = self.page.get_by_text(txt)
            expect(element).to_be_visible(timeout=timeout or self.timeout)
            logger.info(f"断言：文本为 '{txt}' 的元素可见")
            return True
        except Exception as e:
            error_msg = f"断言失败：文本为 '{txt}' 的元素不可见，原因： {e}"
            logger.error(error_msg)
            raise AssertionError(error_msg)

    def assert_innerText_by_css(
        self, selector: str, text_value: str, timeout: int = None
    ) -> bool:
        """
        断言由 CSS 选择器定位的元素的文本内容符合预期。

        Args:
            selector (str): CSS 选择器字符串。
            text_value (str): 期望的文本值。
            timeout (int, optional): 断言的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。

        Returns:
            bool: 如果元素文本符合预期则返回 True，否则抛出异常。
        """
        try:
            element = self.locator_by_css(selector).first
            expect(element).to_have_text(
                text_value,
                timeout=timeout or self.timeout,
            )
            logger.info(f"断言：CSS 选择器为 '{selector}' 的元素文本为 '{text_value}'")
            return True
        except Exception as e:
            error_msg = f"断言失败：CSS 选择器为 '{selector}' 的元素文本不是 '{text_value}'，原因： {e}"
            logger.error(error_msg)
            raise AssertionError(error_msg)

    def assert_innerText_by_role(
        self, role: str, name: str, text_value: str, timeout: int = None
    ) -> bool:
        """
        断言由 ARIA 角色和可访问名称定位的元素的文本内容符合预期。

        Args:
            role (str): 元素的 ARIA 角色。
            name (str): 元素的可见文本或可访问名称。
            text_value (str): 期望的文本值。
            timeout (int, optional): 断言的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。

        Returns:
            bool: 如果元素文本符合预期则返回 True，否则抛出异常。
        """
        try:
            element = self.locator_by_role(role, name)
            expect(element).to_have_text(
                text_value,
                timeout=timeout or self.timeout,
            )
            logger.info(f"断言：role='{role}' 和 name='{name}' 的元素文本为 '{text_value}'")
            return True
        except Exception as e:
            error_msg = f"断言失败：role='{role}' 和 name='{name}' 的元素文本不是 '{text_value}'，原因： {e}"
            logger.error(error_msg)
            raise AssertionError(error_msg)

    def assert_success_message(self, text: str = '提交成功') -> bool:
        """
        断言页面上是否存在指定的成功消息。

        Args:
            text (str, optional): 期望的成功消息文本。默认为 '提交成功'。

        Returns:
            bool: 如果成功消息可见且文本匹配则返回 True，否则抛出异常。
        """
        try:
            css_path = 'div.el-message--success p'
            self.assert_ele_visible_by_css(css_path)
            self.assert_innerText_by_css(css_path, text)
            logger.info(f"断言成功消息：'{text}' 可见")
            return True
        except Exception as e:
            error_msg = f"断言失败：成功消息 '{text}' 不可见，原因: {e}"
            logger.error(error_msg)
            raise AssertionError(error_msg)

    def get_by_label(self, text: str, **kwargs) -> Locator:
        """
        通过元素的关联标签文本获取元素定位器。

        Args:
            text (str): 元素的标签文本。
            **kwargs: 传递给 Playwright `page.get_by_label` 方法的其他参数。

        Returns:
            Locator: Playwright Locator 对象。
        """
        logger.info(f"通过 label='{text}' 查找元素")
        return self.page.get_by_label(text, **kwargs)

    def get_by_test_id(self, test_id: str, **kwargs) -> Locator:
        """
        通过元素的 `data-test-id` 属性获取元素定位器。

        Args:
            test_id (str): 元素的 `data-test-id` 值。
            **kwargs: 传递给 Playwright `page.get_by_test_id` 方法的其他参数。

        Returns:
            Locator: Playwright Locator 对象。
        """
        logger.info(f"通过 test id='{test_id}' 查找元素")
        return self.page.get_by_test_id(test_id, **kwargs)

    def get_by_title(self, title: str, **kwargs) -> Locator:
        """
        通过元素的 title 属性获取元素定位器。

        Args:
            title (str): 元素的 title 属性值。
            **kwargs: 传递给 Playwright `page.get_by_title` 方法的其他参数。

        Returns:
            Locator: Playwright Locator 对象。
        """
        logger.info(f"通过 title='{title}' 查找元素")
        return self.page.get_by_title(title, **kwargs)

    def get_by_alt_text(self, alt_text: str, **kwargs) -> Locator:
        """
        通过图像的 alt 属性获取元素定位器。

        Args:
            alt_text (str): 图像的 alt 属性值。
            **kwargs: 传递给 Playwright `page.get_by_alt_text` 方法的其他参数。

        Returns:
            Locator: Playwright Locator 对象。
        """
        logger.info(f"通过 alt text='{alt_text}' 查找元素")
        return self.page.get_by_alt_text(alt_text, **kwargs)

    def get_by_text(self, text: str, **kwargs) -> Locator:
        """
        通过元素的可见文本内容获取元素定位器。

        Args:
            text (str): 元素的可见文本内容。
            **kwargs: 传递给 Playwright `page.get_by_text` 方法的其他参数。

        Returns:
            Locator: Playwright Locator 对象。
        """
        logger.info(f"通过文本='{text}' 查找元素")
        return self.page.get_by_text(text, **kwargs)

    def get_by_placeholder(self, placeholder: str, **kwargs) -> Locator:
        """
        通过输入框的占位符文本获取元素定位器。

        Args:
            placeholder (str): 输入框的占位符文本。
            **kwargs: 传递给 Playwright `page.get_by_placeholder` 方法的其他参数。

        Returns:
            Locator: Playwright Locator 对象。
        """
        logger.info(f"通过 placeholder='{placeholder}' 查找元素")
        return self.page.get_by_placeholder(placeholder, **kwargs)

    def wait_for_url_change(self, old_url: str, timeout: int = None):
        """
        等待当前页面的 URL 发生变化。

        Args:
            old_url (str): 变化前的旧 URL。
            timeout (int, optional): 等待 URL 变化的超时时间（毫秒）。默认为 None，使用实例的默认超时时间。
        """
        self.page.wait_for_url(
            lambda url: url != old_url, timeout=timeout or self.timeout
        )
        logger.info(f"URL 已从 {old_url} 变为 {self.page.url}")

    def get_current_url(self) -> str:
        """
        获取当前页面的完整 URL。

        Returns:
            str: 当前页面的 URL 字符串。
        """
        return self.page.url
