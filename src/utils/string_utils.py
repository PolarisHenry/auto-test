"""
字符串处理工具类

提供各种字符串操作、验证、转换等实用功能
"""
import random
import re
import hashlib
import base64
import json
import difflib
import string
from typing import List, Optional, Dict, Any, Tuple, Union
from collections import Counter


class StringUtils:
    """字符串处理工具类"""

    @classmethod
    def is_empty(cls, text: str) -> bool:
        """判断字符串是否为空

        Args:
            text: 要检查的字符串

        Returns:
            是否为空字符串
        """
        return text is None or text.strip() == ""

    @classmethod
    def is_not_empty(cls, text: str) -> bool:
        """判断字符串是否不为空

        Args:
            text: 要检查的字符串

        Returns:
            是否不为空字符串
        """
        return not cls.is_empty(text)

    @classmethod
    def safe_strip(cls, text: str, default: str = "") -> str:
        """安全的strip操作，处理None值

        Args:
            text: 要处理的字符串
            default: 默认返回值

        Returns:
            处理后的字符串
        """
        return text.strip() if text is not None else default

    @classmethod
    def truncate(cls, text: str, length: int, suffix: str = "...") -> str:
        """截断字符串到指定长度

        Args:
            text: 原字符串
            length: 目标长度（包含后缀）
            suffix: 后缀字符串

        Returns:
            截断后的字符串
        """
        if not text or len(text) <= length:
            return text

        return text[:length - len(suffix)] + suffix

    @classmethod
    def camel_to_snake(cls, camel_str: str) -> str:
        """驼峰命名转下划线命名

        Args:
            camel_str: 驼峰命名字符串

        Returns:
            下划线命名字符串
        """
        # 在大写字母前加上下划线，然后转为小写
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @classmethod
    def snake_to_camel(cls, snake_str: str) -> str:
        """下划线命名转驼峰命名

        Args:
            snake_str: 下划线命名字符串

        Returns:
            驼峰命名字符串
        """
        components = snake_str.split('_')
        return components[0] + ''.join(word.capitalize() for word in components[1:])

    @classmethod
    def extract_numbers(cls, text: str) -> List[str]:
        """提取字符串中的所有数字

        Args:
            text: 包含数字的字符串

        Returns:
            数字列表
        """
        return re.findall(r'\d+', text)

    @classmethod
    def extract_chinese(cls, text: str) -> str:
        """提取字符串中的中文字符

        Args:
            text: 包含中文的字符串

        Returns:
            纯中文字符串
        """
        return ''.join(re.findall(r'[\u4e00-\u9fff]+', text))

    @classmethod
    def extract_english(cls, text: str) -> str:
        """提取字符串中的英文字符

        Args:
            text: 包含英文的字符串

        Returns:
            纯英文字符串
        """
        return ''.join(re.findall(r'[a-zA-Z]+', text))

    @classmethod
    def count_words(cls, text: str) -> int:
        """统计单词数量

        Args:
            text: 要统计的文本

        Returns:
            单词数量
        """
        if cls.is_empty(text):
            return 0
        return len(text.split())

    @classmethod
    def count_chars(cls, text: str, exclude_spaces: bool = False) -> int:
        """统计字符数量

        Args:
            text: 要统计的文本
            exclude_spaces: 是否排除空格

        Returns:
            字符数量
        """
        if exclude_spaces:
            return len(text.replace(" ", ""))
        return len(text)

    @classmethod
    def most_common_words(cls, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """获取最常见的单词

        Args:
            text: 要分析的文本
            top_n: 返回前N个最常见的单词

        Returns:
            (单词, 出现次数)的列表，按出现次数降序排列
        """
        words = text.lower().split()
        word_counts = Counter(words)
        return word_counts.most_common(top_n)

    @classmethod
    def remove_duplicates(cls, text_list: List[str], case_sensitive: bool = True) -> List[str]:
        """去除字符串列表中的重复项

        Args:
            text_list: 字符串列表
            case_sensitive: 是否大小写敏感

        Returns:
            去重后的列表
        """
        if case_sensitive:
            return list(set(text_list))
        else:
            seen = set()
            result = []
            for item in text_list:
                item_lower = item.lower()
                if item_lower not in seen:
                    seen.add(item_lower)
                    result.append(item)
            return result

    @classmethod
    def find_similar(cls, text: str, text_list: List[str], threshold: float = 0.6) -> List[str]:
        """查找相似的字符串

        Args:
            text: 目标字符串
            text_list: 要搜索的字符串列表
            threshold: 相似度阈值 (0-1之间)

        Returns:
            相似的字符串列表
        """
        similar = []
        for item in text_list:
            similarity = difflib.SequenceMatcher(None, text, item).ratio()
            if similarity >= threshold:
                similar.append(item)
        return similar

    @classmethod
    def mask_sensitive_info(cls, text: str, mask_char: str = "*") -> str:
        """掩盖敏感信息

        Args:
            text: 包含敏感信息的字符串
            mask_char: 掩盖字符

        Returns:
            掩盖后的字符串
        """
        # 掩盖身份证号（15位或18位数字）
        text = re.sub(r'\d{15}(\d{3})?', lambda m: mask_char * (len(m.group()) - 4) + m.group()[-4:], text)
        # 掩盖手机号（11位数字）
        text = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1' + mask_char * 4 + r'\2', text)
        # 掩盖邮箱（@前面的部分）
        text = re.sub(r'(@)', mask_char * 3 + r'\1', text)
        return text

    @classmethod
    def format_phone(cls, phone: str) -> str:
        """格式化手机号显示

        Args:
            phone: 手机号

        Returns:
            格式化的手机号（如：138 1234 5678）
        """
        phone = re.sub(r'\D', '', phone)  # 只保留数字
        if len(phone) == 11:
            return f"{phone[:3]} {phone[3:7]} {phone[7:]}"
        return phone

    @classmethod
    def format_id_card(cls, id_card: str) -> str:
        """格式化身份证号显示

        Args:
            id_card: 身份证号

        Returns:
            格式化的身份证号（如：123456 123456789 123X）
        """
        id_card = re.sub(r'\D', '', id_card)  # 只保留数字和X
        if len(id_card) == 18:
            return f"{id_card[:6]} {id_card[6:14]} {id_card[14:]}"
        elif len(id_card) == 15:
            return f"{id_card[:6]} {id_card[6:12]} {id_card[12:]}"
        return id_card

    @classmethod
    def is_valid_phone(cls, phone: str) -> bool:
        """验证手机号格式

        Args:
            phone: 手机号

        Returns:
            是否为有效手机号
        """
        phone_pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(phone_pattern, phone))

    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        """验证邮箱格式

        Args:
            email: 邮箱地址

        Returns:
            是否为有效邮箱
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))

    @classmethod
    def is_valid_id_card(cls, id_card: str) -> bool:
        """验证身份证号格式

        Args:
            id_card: 身份证号

        Returns:
            是否为有效身份证号
        """
        # 15位身份证号
        pattern_15 = r'^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$'
        # 18位身份证号
        pattern_18 = r'^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}[0-9Xx]$'

        return bool(re.match(pattern_15, id_card)) or bool(re.match(pattern_18, id_card))

    @classmethod
    def generate_random_string(cls, length: int, charset: str = "all") -> str:
        """生成随机字符串

        Args:
            length: 字符串长度
            charset: 字符集类型
                - "digit": 纯数字
                - "letter": 纯字母
                - "lower": 小写字母
                - "upper": 大写字母
                - "all": 数字+字母+特殊字符

        Returns:
            随机字符串
        """
        if charset == "digit":
            chars = string.digits
        elif charset == "letter":
            chars = string.ascii_letters
        elif charset == "lower":
            chars = string.ascii_lowercase
        elif charset == "upper":
            chars = string.ascii_uppercase
        else:  # "all"
            chars = string.ascii_letters + string.digits + "!@#$%^&*"

        return ''.join(random.choice(chars) for _ in range(length))

    @classmethod
    def encode_base64(cls, text: str, encoding: str = 'utf-8') -> str:
        """Base64编码

        Args:
            text: 要编码的字符串
            encoding: 字符编码

        Returns:
            Base64编码后的字符串
        """
        encoded_bytes = text.encode(encoding)
        encoded_str = base64.b64encode(encoded_bytes)
        return encoded_str.decode(encoding)

    @classmethod
    def decode_base64(cls, encoded_text: str, encoding: str = 'utf-8') -> str:
        """Base64解码

        Args:
            encoded_text: 要解码的Base64字符串
            encoding: 字符编码

        Returns:
            解码后的字符串
        """
        decoded_bytes = base64.b64decode(encoded_text)
        return decoded_bytes.decode(encoding)

    @classmethod
    def md5_hash(cls, text: str, encoding: str = 'utf-8') -> str:
        """计算MD5哈希值

        Args:
            text: 要计算哈希的字符串
            encoding: 字符编码

        Returns:
            MD5哈希值（十六进制字符串）
        """
        return hashlib.md5(text.encode(encoding)).hexdigest()

    @classmethod
    def sha256_hash(cls, text: str, encoding: str = 'utf-8') -> str:
        """计算SHA256哈希值

        Args:
            text: 要计算哈希的字符串
            encoding: 字符编码

        Returns:
            SHA256哈希值（十六进制字符串）
        """
        return hashlib.sha256(text.encode(encoding)).hexdigest()

    @classmethod
    def remove_html_tags(cls, html_text: str) -> str:
        """移除HTML标签

        Args:
            html_text: 包含HTML标签的字符串

        Returns:
            纯文本字符串
        """
        return re.sub(r'<[^>]+>', '', html_text)

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """提取文本中的URL

        Args:
            text: 包含URL的文本

        Returns:
            URL列表
        """
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w)*)?)?'
        return re.findall(url_pattern, text)

    @classmethod
    def word_frequency(cls, text: str) -> Dict[str, int]:
        """统计单词频率

        Args:
            text: 要分析的文本

        Returns:
            单词频率字典
        """
        words = re.findall(r'\b\w+\b', text.lower())
        return dict(Counter(words))

    @classmethod
    def levenshtein_distance(cls, str1: str, str2: str) -> int:
        """计算编辑距离

        Args:
            str1: 字符串1
            str2: 字符串2

        Returns:
            编辑距离
        """
        if len(str1) < len(str2):
            return cls.levenshtein_distance(str2, str1)

        if len(str2) == 0:
            return len(str1)

        previous_row = list(range(len(str2) + 1))
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @classmethod
    def similarity_ratio(cls, str1: str, str2: str) -> float:
        """计算字符串相似度

        Args:
            str1: 字符串1
            str2: 字符串2

        Returns:
            相似度 (0-1之间)
        """
        return difflib.SequenceMatcher(None, str1, str2).ratio()

    @classmethod
    def format_json_str(cls, json_str: str, indent: int = 4) -> str:
        """格式化JSON字符串

        Args:
            json_str: JSON字符串
            indent: 缩进空格数

        Returns:
            格式化后的JSON字符串
        """
        try:
            parsed = json.loads(json_str)
            return json.dumps(parsed, indent=indent, ensure_ascii=False)
        except json.JSONDecodeError:
            return json_str

    @classmethod
    def pad_string(cls, text: str, width: int, align: str = 'left', pad_char: str = ' ') -> str:
        """填充字符串到指定宽度

        Args:
            text: 原字符串
            width: 目标宽度
            align: 对齐方式 ('left', 'right', 'center')
            pad_char: 填充字符

        Returns:
            填充后的字符串
        """
        if len(text) >= width:
            return text

        if align == 'left':
            return text.ljust(width, pad_char)
        elif align == 'right':
            return text.rjust(width, pad_char)
        elif align == 'center':
            return text.center(width, pad_char)
        else:
            return text

    @classmethod
    def split_by_length(cls, text: str, chunk_size: int) -> List[str]:
        """按长度分割字符串

        Args:
            text: 要分割的字符串
            chunk_size: 每块大小

        Returns:
            分割后的字符串列表
        """
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    @classmethod
    def remove_extra_spaces(cls, text: str) -> str:
        """移除多余的空格

        Args:
            text: 要处理的字符串

        Returns:
            处理后的字符串
        """
        return re.sub(r'\s+', ' ', text.strip())