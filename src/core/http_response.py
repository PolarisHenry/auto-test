import re
import jmespath
from loguru import logger
import requests


class CustomResponse(requests.Response):
    def __init__(self, response):
        super().__init__()
        self.__dict__.update(response.__dict__)

    def search(self, expression):
        """
        使用JMESPath表达式从响应内容中提取数据

        Args:
            expression (str): JMESPath表达式

        Returns:
            匹配的数据，如果未找到则返回None

        Raises:
            Exception: 当JSON解析失败或JMESPath表达式无效时抛出
        """
        try:
            json_data = self.json()  # 尝试将响应内容解析为JSON
            result = jmespath.search(expression, json_data)
            logger.info(
                f"[JMESPath搜索] 表达式: {expression}, [搜索结果] {result}"
            )
            return result
        except Exception as e:
            logger.error(f"[JMESPath错误] JSON解析失败或表达式无效，expression: {expression}，错误详情: {e}")
            raise

    def find_all(self, pattern):
        """
        使用正则表达式查找响应内容中的所有匹配项

        Args:
            pattern (str): 正则表达式模式

        Returns:
            list: 所有匹配的结果列表，如果未找到则返回空列表

        Raises:
            (ValueError, TypeError): 当响应内容为空或正则表达式无效时抛出
        """
        try:
            result = re.findall(pattern, self.text)
            logger.info(
                f"[正则查找全部] 模式: {pattern}\n[匹配结果] 找到 {len(result)} 个匹配项: {result}"
            )
            return result
        except (ValueError, TypeError) as e:
            logger.error(f"[正则表达式错误] 响应内容无法解析或正则表达式无效，pattern: {pattern}，错误详情: {e}")
            raise

    def find_one(self, pattern):
        """
        使用正则表达式查找响应内容中的第一个匹配项

        Args:
            pattern (str): 正则表达式模式

        Returns:
            str or None: 第一个匹配的结果，如果未找到则返回None

        Raises:
            Exception: 当响应内容为空或正则表达式无效时抛出
        """
        try:
            matches = re.findall(pattern, self.text)
            if not matches:
                logger.warning(f"[正则查找单个] 未找到匹配项，pattern: {pattern}")
                return None
            result = matches[0]
            logger.info(
                f"[正则查找单个] 模式: {pattern}\n[匹配结果] {result}"
            )
            return result
        except Exception as e:
            logger.error(f"[正则表达式错误] 响应内容无法解析或正则表达式无效，pattern: {pattern}，错误详情: {e}")
            raise

    def re_search(self, pattern):
        """
        使用正则表达式查找响应内容中的第一个捕获组

        Args:
            pattern (str): 正则表达式模式，必须包含至少一个捕获组

        Returns:
            str or None: 第一个捕获组的内容，如果未找到则返回None

        Raises:
            (ValueError, AttributeError, IndexError): 当响应内容为空、正则表达式无效或无捕获组时抛出
        """
        try:
            match = re.search(pattern, self.text)
            if not match:
                logger.warning(f"[正则搜索捕获组] 未找到匹配项，pattern: {pattern}")
                return None
            result = match.group(1)
            logger.info(
                f"[正则搜索捕获组] 模式: {pattern}\n[捕获组内容] {result}"
            )
            return result
        except (ValueError, AttributeError, IndexError) as e:
            logger.error(f"[正则表达式错误] 响应内容无法解析、正则表达式无效或无捕获组，pattern: {pattern}，错误详情: {e}")
            raise
