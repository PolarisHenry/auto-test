"""
数字处理工具类

提供各种数字验证、格式化、计算等实用功能
"""
import math
import decimal
import random
from typing import List, Optional, Union, Tuple


class NumberUtils:
    """数字处理工具类"""

    @classmethod
    def is_number(cls, value: str) -> bool:
        """判断字符串是否为数字

        Args:
            value: 要检查的值

        Returns:
            是否为数字
        """
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    @classmethod
    def is_int(cls, value: str) -> bool:
        """判断字符串是否为整数

        Args:
            value: 要检查的值

        Returns:
            是否为整数
        """
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    @classmethod
    def is_positive_number(cls, value: Union[str, int, float]) -> bool:
        """判断是否为正数

        Args:
            value: 要检查的值

        Returns:
            是否为正数
        """
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False

    @classmethod
    def is_negative_number(cls, value: Union[str, int, float]) -> bool:
        """判断是否为负数

        Args:
            value: 要检查的值

        Returns:
            是否为负数
        """
        try:
            num = float(value)
            return num < 0
        except (ValueError, TypeError):
            return False

    @classmethod
    def is_even(cls, value: int) -> bool:
        """判断是否为偶数

        Args:
            value: 要检查的整数

        Returns:
            是否为偶数
        """
        return value % 2 == 0

    @classmethod
    def is_odd(cls, value: int) -> bool:
        """判断是否为奇数

        Args:
            value: 要检查的整数

        Returns:
            是否为奇数
        """
        return value % 2 != 0

    @classmethod
    def is_prime(cls, value: int) -> bool:
        """判断是否为质数

        Args:
            value: 要检查的整数

        Returns:
            是否为质数
        """
        if value < 2:
            return False
        if value == 2:
            return True
        if value % 2 == 0:
            return False

        for i in range(3, int(math.sqrt(value)) + 1, 2):
            if value % i == 0:
                return False
        return True

    @classmethod
    def format_number(cls, value: Union[int, float], decimal_places: int = 2) -> str:
        """格式化数字显示

        Args:
            value: 要格式化的数字
            decimal_places: 小数位数

        Returns:
            格式化后的字符串
        """
        return f"{value:,.{decimal_places}f}"

    @classmethod
    def format_percentage(cls, value: Union[int, float], decimal_places: int = 1) -> str:
        """格式化为百分比

        Args:
            value: 要格式化的数字（0.25 表示 25%）
            decimal_places: 小数位数

        Returns:
            百分比字符串（如：25.0%）
        """
        return f"{value*100:.{decimal_places}f}%"

    @classmethod
    def format_currency(cls, value: Union[int, float], currency: str = "¥") -> str:
        """格式化为货币显示

        Args:
            value: 金额数字
            currency: 货币符号

        Returns:
            货币字符串（如：¥1,234.56）
        """
        return f"{currency}{value:,}"

    @classmethod
    def format_file_size(cls, size_bytes: int) -> str:
        """格式化文件大小

        Args:
            size_bytes: 文件大小（字节）

        Returns:
            格式化的文件大小（如：1.2 MB）
        """
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
        size_index = 0
        while size_bytes >= 1024 and size_index < len(size_names) - 1:
            size_bytes /= 1024.0
            size_index += 1

        return f"{size_bytes:.1f} {size_names[size_index]}"

    @classmethod
    def round_half_up(cls, value: Union[int, float], decimal_places: int = 0) -> float:
        """四舍五入（遇到.5向上取整）

        Args:
            value: 要处理的数字
            decimal_places: 小数位数

        Returns:
            四舍五入后的数字
        """
        multiplier = 10 ** decimal_places
        return math.floor(value * multiplier + 0.5) / multiplier

    @classmethod
    def round_half_down(cls, value: Union[int, float], decimal_places: int = 0) -> float:
        """四舍五入（遇到.5向下取整）

        Args:
            value: 要处理的数字
            decimal_places: 小数位数

        Returns:
            四舍五入后的数字
        """
        multiplier = 10 ** decimal_places
        return math.ceil(value * multiplier - 0.5) / multiplier

    @classmethod
    def clamp(cls, value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
        """限制数字在指定范围内

        Args:
            value: 要限制的数字
            min_val: 最小值
            max_val: 最大值

        Returns:
            限制后的数字
        """
        return max(min_val, min(value, max_val))

    @classmethod
    def lerp(cls, start: Union[int, float], end: Union[int, float], factor: float) -> Union[int, float]:
        """线性插值

        Args:
            start: 起始值
            end: 结束值
            factor: 插值因子（0-1之间）

        Returns:
            插值结果
        """
        return start + (end - start) * cls.clamp(factor, 0.0, 1.0)

    @classmethod
    def percentage_change(cls, old_value: Union[int, float], new_value: Union[int, float]) -> float:
        """计算百分比变化

        Args:
            old_value: 原值
            new_value: 新值

        Returns:
            百分比变化（正数表示增长，负数表示减少）
        """
        if old_value == 0:
            return 0.0 if new_value == 0 else float('inf')

        return ((new_value - old_value) / abs(old_value)) * 100

    @classmethod
    def safe_divide(cls, dividend: Union[int, float], divisor: Union[int, float], default: Union[int, float] = 0) -> Union[int, float]:
        """安全的除法运算

        Args:
            dividend: 被除数
            divisor: 除数
            default: 除数为0时的默认返回值

        Returns:
            除法结果
        """
        try:
            return dividend / divisor
        except ZeroDivisionError:
            return default

    @classmethod
    def average(cls, numbers: List[Union[int, float]]) -> float:
        """计算平均值

        Args:
            numbers: 数字列表

        Returns:
            平均值
        """
        if not numbers:
            return 0.0
        return sum(numbers) / len(numbers)

    @classmethod
    def median(cls, numbers: List[Union[int, float]]) -> float:
        """计算中位数

        Args:
            numbers: 数字列表

        Returns:
            中位数
        """
        if not numbers:
            return 0.0

        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            return sorted_numbers[n//2]

    @classmethod
    def mode(cls, numbers: List[Union[int, float]]) -> List[Union[int, float]]:
        """计算众数

        Args:
            numbers: 数字列表

        Returns:
            众数列表（可能有多个）
        """
        if not numbers:
            return []

        from collections import Counter
        count = Counter(numbers)
        max_freq = max(count.values())
        return [num for num, freq in count.items() if freq == max_freq]

    @classmethod
    def variance(cls, numbers: List[Union[int, float]]) -> float:
        """计算方差

        Args:
            numbers: 数字列表

        Returns:
            方差
        """
        if len(numbers) < 2:
            return 0.0

        mean = cls.average(numbers)
        return sum((x - mean) ** 2 for x in numbers) / len(numbers)

    @classmethod
    def standard_deviation(cls, numbers: List[Union[int, float]]) -> float:
        """计算标准差

        Args:
            numbers: 数字列表

        Returns:
            标准差
        """
        return math.sqrt(cls.variance(numbers))

    @classmethod
    def normalize(cls, value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> float:
        """归一化到0-1之间

        Args:
            value: 要归一化的值
            min_val: 最小值
            max_val: 最大值

        Returns:
            归一化后的值（0-1之间）
        """
        if min_val == max_val:
            return 0.0
        return (value - min_val) / (max_val - min_val)

    @classmethod
    def denormalize(cls, normalized_value: float, min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
        """反归一化

        Args:
            normalized_value: 归一化值（0-1之间）
            min_val: 原始最小值
            max_val: 原始最大值

        Returns:
            反归一化后的值
        """
        return normalized_value * (max_val - min_val) + min_val

    @classmethod
    def round_to_nearest(cls, value: Union[int, float], base: Union[int, float]) -> Union[int, float]:
        """舍入到最接近的基数倍

        Args:
            value: 要舍入的值
            base: 基数

        Returns:
            舍入后的值
        """
        return round(value / base) * base

    @classmethod
    def factorial(cls, n: int) -> int:
        """计算阶乘

        Args:
            n: 非负整数

        Returns:
            阶乘结果
        """
        if n < 0:
            raise ValueError("阶乘只定义在非负整数上")
        return math.factorial(n)

    @classmethod
    def combination(cls, n: int, k: int) -> int:
        """计算组合数 C(n,k)

        Args:
            n: 总数
            k: 选择数

        Returns:
            组合数结果
        """
        if n < 0 or k < 0 or k > n:
            return 0
        return cls.factorial(n) // (cls.factorial(k) * cls.factorial(n - k))

    @classmethod
    def permutation(cls, n: int, k: int) -> int:
        """计算排列数 P(n,k)

        Args:
            n: 总数
            k: 选择数

        Returns:
            排列数结果
        """
        if n < 0 or k < 0 or k > n:
            return 0
        return cls.factorial(n) // cls.factorial(n - k)

    @classmethod
    def is_within_tolerance(cls, value1: Union[int, float], value2: Union[int, float], tolerance: float = 1e-6) -> bool:
        """判断两个数值是否在容差范围内相等

        Args:
            value1: 数值1
            value2: 数值2
            tolerance: 容差值

        Returns:
            是否相等（在容差范围内）
        """
        return abs(value1 - value2) <= tolerance

    @classmethod
    def generate_random_int(cls, min_val: int = 1, max_val: int = 100) -> int:
        """生成随机整数

        Args:
            min_val: 最小值
            max_val: 最大值

        Returns:
            随机整数
        """
        return random.randint(min_val, max_val)

    @classmethod
    def generate_random_float(cls, min_val: float = 0.0, max_val: float = 1.0, decimal_places: int = 2) -> float:
        """生成随机浮点数

        Args:
            min_val: 最小值
            max_val: 最大值
            decimal_places: 小数位数

        Returns:
            随机浮点数
        """
        value = random.uniform(min_val, max_val)
        return round(value, decimal_places)

    @classmethod
    def format_phone(cls, phone: str) -> str:
        """格式化手机号

        Args:
            phone: 手机号字符串

        Returns:
            格式化的手机号（如：138 1234 5678）
        """
        # 移除所有非数字字符
        digits = ''.join(filter(str.isdigit, str(phone)))

        if len(digits) == 11:
            return f"{digits[:3]} {digits[3:7]} {digits[7:]}"
        return digits

    @classmethod
    def format_id_card(cls, id_card: str) -> str:
        """格式化身份证号

        Args:
            id_card: 身份证号字符串

        Returns:
            格式化的身份证号
        """
        # 移除所有非数字和X字符
        cleaned = ''.join(c for c in str(id_card) if c.isdigit() or c.upper() == 'X')

        if len(cleaned) == 18:
            return f"{cleaned[:6]} {cleaned[6:14]} {cleaned[14:]}"
        elif len(cleaned) == 15:
            return f"{cleaned[:6]} {cleaned[6:12]} {cleaned[12:]}"
        return cleaned

    @classmethod
    def calculate_bmi(cls, weight_kg: Union[int, float], height_m: Union[int, float]) -> float:
        """计算BMI指数

        Args:
            weight_kg: 体重（公斤）
            height_m: 身高（米）

        Returns:
            BMI指数
        """
        if height_m <= 0:
            raise ValueError("身高必须大于0")
        return weight_kg / (height_m ** 2)

    @classmethod
    def calculate_bmi_category(cls, bmi: float) -> str:
        """根据BMI值获取分类

        Args:
            bmi: BMI指数

        Returns:
            BMI分类
        """
        if bmi < 18.5:
            return "偏瘦"
        elif bmi < 24:
            return "正常"
        elif bmi < 28:
            return "偏胖"
        else:
            return "肥胖"

    @classmethod
    def generate_luhn_checksum(cls, number: str) -> int:
        """生成Luhn校验码（用于银行卡验证）

        Args:
            number: 卡号前缀（不包含校验位）

        Returns:
            校验位数字
        """
        digits = [int(d) for d in str(number)]
        digits.reverse()

        total = 0
        for i, digit in enumerate(digits):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit

        return (10 - (total % 10)) % 10

    @classmethod
    def validate_luhn(cls, number: str) -> bool:
        """验证Luhn校验码（银行卡验证）

        Args:
            number: 完整的卡号（包含校验位）

        Returns:
            是否通过Luhn验证
        """
        digits = [int(d) for d in str(number)]
        if len(digits) < 2:
            return False

        # 分离校验位
        checksum = digits[-1]
        digits = digits[:-1]

        # 计算应有的校验位
        expected_checksum = cls.generate_luhn_checksum(''.join(map(str, digits)))

        return checksum == expected_checksum

    @classmethod
    def format_scientific_notation(cls, value: Union[int, float], precision: int = 2) -> str:
        """格式化为科学计数法

        Args:
            value: 要格式化的数字
            precision: 精度（小数位数）

        Returns:
            科学计数法字符串
        """
        return f"{value:.{precision}e}"

    @classmethod
    def parse_scientific_notation(cls, sci_str: str) -> float:
        """解析科学计数法字符串

        Args:
            sci_str: 科学计数法字符串（如：1.23e+04）

        Returns:
            解析后的浮点数
        """
        return float(sci_str)

    @classmethod
    def format_duration(cls, total_seconds: int) -> str:
        """格式化时长显示

        Args:
            total_seconds: 总秒数

        Returns:
            格式化的时长字符串（如：2天 3小时 45分钟 30秒）
        """
        if total_seconds < 0:
            return "负数时长"

        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days:
            parts.append(f"{days}天")
        if hours:
            parts.append(f"{hours}小时")
        if minutes:
            parts.append(f"{minutes}分钟")
        if seconds or not parts:
            parts.append(f"{seconds}秒")

        return " ".join(parts)

    @classmethod
    def calculate_percentage_of_total(cls, part: Union[int, float], total: Union[int, float]) -> float:
        """计算部分占总体的百分比

        Args:
            part: 部分值
            total: 总体值

        Returns:
            百分比（0-100之间）
        """
        if total == 0:
            return 0.0
        return (part / total) * 100

    @classmethod
    def is_leap_year(cls, year: int) -> bool:
        """判断是否为闰年

        Args:
            year: 年份

        Returns:
            是否为闰年
        """
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @classmethod
    def days_in_month(cls, year: int, month: int) -> int:
        """获取指定月份的天数

        Args:
            year: 年份
            month: 月份

        Returns:
            该月的天数
        """
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if month == 2 and cls.is_leap_year(year):
            return 29

        return days_in_month[month - 1]

    @classmethod
    def roman_to_int(cls, roman: str) -> int:
        """罗马数字转整数

        Args:
            roman: 罗马数字字符串

        Returns:
            整数值
        """
        roman_values = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

        total = 0
        prev_value = 0

        for char in reversed(roman.upper()):
            value = roman_values.get(char, 0)
            if value == 0:
                raise ValueError(f"无效的罗马数字字符: {char}")

            if value < prev_value:
                total -= value
            else:
                total += value

            prev_value = value

        return total

    @classmethod
    def int_to_roman(cls, num: int) -> str:
        """整数转罗马数字

        Args:
            num: 整数（1-3999）

        Returns:
            罗马数字字符串
        """
        if not (1 <= num <= 3999):
            raise ValueError("只能转换1-3999之间的数字")

        roman_numerals = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]

        result = []
        for value, numeral in roman_numerals:
            while num >= value:
                result.append(numeral)
                num -= value

        return ''.join(result)