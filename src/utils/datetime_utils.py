"""
时间处理工具类

提供各种时间格式转换、时间计算、时间验证等实用功能
"""
import time
import datetime
from typing import Optional, Union, Tuple
from dateutil.relativedelta import relativedelta


class DateTimeUtils:
    """时间处理工具类"""

    # 常用的时间格式
    FORMAT_YMD = "%Y-%m-%d"
    FORMAT_YMD_HMS = "%Y-%m-%d %H:%M:%S"
    FORMAT_YMD_HM = "%Y-%m-%d %H:%M"
    FORMAT_HMS = "%H:%M:%S"
    FORMAT_TIMESTAMP = "%Y-%m-%d %H:%M:%S.%f"

    @classmethod
    def now_str(cls, format_str: str = FORMAT_YMD_HMS) -> str:
        """获取当前时间字符串

        Args:
            format_str: 时间格式

        Returns:
            格式化的当前时间字符串
        """
        return datetime.datetime.now().strftime(format_str)

    @classmethod
    def today_str(cls, format_str: str = FORMAT_YMD) -> str:
        """获取今天日期字符串

        Args:
            format_str: 日期格式

        Returns:
            格式化的今天日期字符串
        """
        return datetime.date.today().strftime(format_str)

    @classmethod
    def str_to_datetime(cls, time_str: str, format_str: str = FORMAT_YMD_HMS) -> datetime.datetime:
        """字符串转datetime对象

        Args:
            time_str: 时间字符串
            format_str: 时间格式

        Returns:
            datetime对象
        """
        return datetime.datetime.strptime(time_str, format_str)

    @classmethod
    def datetime_to_str(cls, dt: datetime.datetime, format_str: str = FORMAT_YMD_HMS) -> str:
        """datetime对象转字符串

        Args:
            dt: datetime对象
            format_str: 时间格式

        Returns:
            格式化的时间字符串
        """
        return dt.strftime(format_str)

    @classmethod
    def timestamp_to_str(cls, timestamp: float, format_str: str = FORMAT_YMD_HMS) -> str:
        """时间戳转字符串

        Args:
            timestamp: 时间戳（秒）
            format_str: 时间格式

        Returns:
            格式化的时间字符串
        """
        return datetime.datetime.fromtimestamp(timestamp).strftime(format_str)

    @classmethod
    def str_to_timestamp(cls, time_str: str, format_str: str = FORMAT_YMD_HMS) -> float:
        """字符串转时间戳

        Args:
            time_str: 时间字符串
            format_str: 时间格式

        Returns:
            时间戳（秒）
        """
        dt = cls.str_to_datetime(time_str, format_str)
        return time.mktime(dt.timetuple())

    @classmethod
    def get_time_diff(cls, start_time: str, end_time: str, format_str: str = FORMAT_YMD_HMS) -> dict:
        """计算两个时间的时间差

        Args:
            start_time: 开始时间字符串
            end_time: 结束时间字符串
            format_str: 时间格式

        Returns:
            包含各种时间差的字典
        """
        start_dt = cls.str_to_datetime(start_time, format_str)
        end_dt = cls.str_to_datetime(end_time, format_str)

        diff = end_dt - start_dt

        return {
            'days': diff.days,
            'seconds': diff.seconds,
            'microseconds': diff.microseconds,
            'total_seconds': diff.total_seconds(),
            'hours': diff.seconds // 3600,
            'minutes': (diff.seconds % 3600) // 60
        }

    @classmethod
    def add_time(cls, time_str: str, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0,
                 format_str: str = FORMAT_YMD_HMS) -> str:
        """时间加法运算

        Args:
            time_str: 基准时间字符串
            days: 天数
            hours: 小时数
            minutes: 分钟数
            seconds: 秒数
            format_str: 时间格式

        Returns:
            计算后的时间字符串
        """
        dt = cls.str_to_datetime(time_str, format_str)

        # 使用 relativedelta 处理月份和年份的进位
        new_dt = dt + relativedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

        return cls.datetime_to_str(new_dt, format_str)

    @classmethod
    def is_valid_date(cls, date_str: str, format_str: str = FORMAT_YMD) -> bool:
        """验证日期字符串是否有效

        Args:
            date_str: 日期字符串
            format_str: 日期格式

        Returns:
            是否为有效日期
        """
        try:
            datetime.datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            return False

    @classmethod
    def get_age(cls, birth_date: str, format_str: str = FORMAT_YMD) -> int:
        """根据出生日期计算年龄

        Args:
            birth_date: 出生日期字符串
            format_str: 日期格式

        Returns:
            年龄（岁）
        """
        birth_dt = cls.str_to_datetime(birth_date, format_str)
        today = datetime.date.today()
        age = today.year - birth_dt.year

        # 如果还没到生日，年龄减一
        if (today.month, today.day) < (birth_dt.month, birth_dt.day):
            age -= 1

        return age

    @classmethod
    def format_duration(cls, total_seconds: int) -> str:
        """格式化时长显示

        Args:
            total_seconds: 总秒数

        Returns:
            格式化的时长字符串（如：2天 3小时 45分钟 30秒）
        """
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
    def get_weekday_cn(cls, date_str: str, format_str: str = FORMAT_YMD) -> str:
        """获取中文星期几

        Args:
            date_str: 日期字符串
            format_str: 日期格式

        Returns:
            中文星期几
        """
        weekdays_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        dt = cls.str_to_datetime(date_str, format_str)
        return weekdays_cn[dt.weekday()]

    @classmethod
    def is_workday(cls, date_str: str, format_str: str = FORMAT_YMD) -> bool:
        """判断是否为工作日

        Args:
            date_str: 日期字符串
            format_str: 日期格式

        Returns:
            是否为工作日（周一到周五）
        """
        dt = cls.str_to_datetime(date_str, format_str)
        return dt.weekday() < 5  # 0-4 表示周一到周五

    @classmethod
    def get_month_range(cls, year: int, month: int) -> Tuple[str, str]:
        """获取指定月份的开始和结束日期

        Args:
            year: 年份
            month: 月份

        Returns:
            (开始日期, 结束日期)的元组
        """
        start_date = datetime.date(year, month, 1)
        if month == 12:
            end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        return (start_date.strftime(cls.FORMAT_YMD), end_date.strftime(cls.FORMAT_YMD))