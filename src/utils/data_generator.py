"""
数据生成工具类

提供各种测试数据生成功能，包括中文人名、地址、电话号码等
"""
import datetime
import random
import string
from typing import List, Optional, Dict, Any
from faker import Faker


class DataGenerator:
    """数据生成工具类"""

    def __init__(self, locale: str = 'zh_CN'):
        """初始化数据生成器

        Args:
            locale: 语言环境，默认中文
        """
        self.faker = Faker(locale)

    # ==================== 人名生成 ====================

    def chinese_name(self, gender: Optional[str] = None) -> str:
        """生成中文人名

        Args:
            gender: 性别，'male'/'female'/None

        Returns:
            中文人名
        """
        if gender == 'male':
            return self.faker.name_male()
        elif gender == 'female':
            return self.faker.name_female()
        else:
            return self.faker.name()

    def english_name(self, gender: Optional[str] = None) -> str:
        """生成英文人名

        Args:
            gender: 性别，'male'/'female'/None

        Returns:
            英文人名
        """
        if gender == 'male':
            return self.faker.first_name_male() + " " + self.faker.last_name()
        elif gender == 'female':
            return self.faker.first_name_female() + " " + self.faker.last_name()
        else:
            return self.faker.first_name() + " " + self.faker.last_name()

    def batch_chinese_names(self, count: int, gender: Optional[str] = None) -> List[str]:
        """批量生成中文人名

        Args:
            count: 生成数量
            gender: 性别偏好

        Returns:
            人名列表
        """
        return [self.chinese_name(gender) for _ in range(count)]

    # ==================== 联系方式生成 ====================

    def phone_number(self) -> str:
        """生成手机号

        Returns:
            手机号字符串
        """
        return self.faker.phone_number()

    def telephone(self) -> str:
        """生成座机号

        Returns:
            座机号字符串
        """
        return self.faker.phone_number()

    def email(self, domain: Optional[str] = None) -> str:
        """生成邮箱地址

        Args:
            domain: 邮箱域名，如果为None则随机生成

        Returns:
            邮箱地址
        """
        if domain:
            username = self.faker.user_name()
            return f"{username}@{domain}"
        else:
            return self.faker.email()

    def batch_phone_numbers(self, count: int) -> List[str]:
        """批量生成手机号

        Args:
            count: 生成数量

        Returns:
            手机号列表
        """
        return [self.phone_number() for _ in range(count)]

    # ==================== 地址生成 ====================

    def chinese_address(self) -> str:
        """生成中文地址

        Returns:
            中文地址字符串
        """
        return self.faker.address()

    def province(self) -> str:
        """生成省份名称

        Returns:
            省份名称
        """
        provinces = [
            "北京市", "上海市", "天津市", "重庆市", "河北省", "山西省", "辽宁省", "吉林省",
            "黑龙江省", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省",
            "湖北省", "湖南省", "广东省", "海南省", "四川省", "贵州省", "云南省", "陕西省",
            "甘肃省", "青海省", "台湾省", "内蒙古自治区", "广西壮族自治区", "西藏自治区",
            "宁夏回族自治区", "新疆维吾尔自治区", "香港特别行政区", "澳门特别行政区"
        ]
        return random.choice(provinces)

    def city(self) -> str:
        """生成城市名称

        Returns:
            城市名称
        """
        cities = [
            "北京市", "上海市", "深圳市", "广州市", "成都市", "杭州市", "武汉市", "南京市",
            "西安市", "青岛市", "大连市", "宁波市", "厦门市", "哈尔滨市", "长春市", "沈阳市",
            "济南市", "福州市", "南昌市", "郑州市", "长沙市", "南宁市", "昆明市", "贵阳市",
            "兰州市", "西宁市", "银川市", "乌鲁木齐市", "拉萨市", "呼和浩特市"
        ]
        return random.choice(cities)

    def district(self) -> str:
        """生成区县名称

        Returns:
            区县名称
        """
        districts = [
            "朝阳区", "海淀区", "西城区", "东城区", "丰台区", "石景山区", "门头沟区", "房山区",
            "通州区", "顺义区", "昌平区", "大兴区", "怀柔区", "平谷区", "密云区", "延庆区",
            "浦东新区", "黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区", "杨浦区",
            "闵行区", "宝山区", "嘉定区", "金山区", "松江区", "青浦区", "奉贤区", "崇明区"
        ]
        return random.choice(districts)

    # ==================== 身份证号生成 ====================

    def id_card(self) -> str:
        """生成身份证号

        Returns:
            身份证号字符串
        """
        return self.faker.ssn()

    def batch_id_cards(self, count: int) -> List[str]:
        """批量生成身份证号

        Args:
            count: 生成数量

        Returns:
            身份证号列表
        """
        return [self.id_card() for _ in range(count)]

    # ==================== 数字和编号生成 ====================

    def random_int(self, min_val: int = 1, max_val: int = 1000) -> int:
        """生成随机整数

        Args:
            min_val: 最小值
            max_val: 最大值

        Returns:
            随机整数
        """
        return random.randint(min_val, max_val)

    def random_float(self, min_val: float = 0.0, max_val: float = 1000.0, decimal: int = 2) -> float:
        """生成随机浮点数

        Args:
            min_val: 最小值
            max_val: 最大值
            decimal: 小数位数

        Returns:
            随机浮点数
        """
        value = random.uniform(min_val, max_val)
        return round(value, decimal)

    def order_number(self, prefix: str = "ORD", length: int = 8) -> str:
        """生成订单号

        Args:
            prefix: 前缀
            length: 编号长度（不包括前缀）

        Returns:
            订单号
        """
        suffix = ''.join(random.choices(string.digits, k=length))
        return f"{prefix}{suffix}"

    def batch_order_numbers(self, count: int, prefix: str = "ORD", length: int = 8) -> List[str]:
        """批量生成订单号

        Args:
            count: 生成数量
            prefix: 前缀
            length: 编号长度

        Returns:
            订单号列表
        """
        return [self.order_number(prefix, length) for _ in range(count)]

    # ==================== 文本内容生成 ====================

    def random_text(self, min_length: int = 10, max_length: int = 100) -> str:
        """生成随机文本

        Args:
            min_length: 最小长度
            max_length: 最大长度

        Returns:
            随机文本
        """
        length = random.randint(min_length, max_length)
        return self.faker.text(length)[:length]

    def sentence(self, min_words: int = 5, max_words: int = 20) -> str:
        """生成随机句子

        Args:
            min_words: 最少单词数
            max_words: 最多单词数

        Returns:
            随机句子
        """
        words = random.randint(min_words, max_words)
        return self.faker.sentence(nb_words=words)

    def company_name(self) -> str:
        """生成公司名称

        Returns:
            公司名称
        """
        return self.faker.company()

    def job_title(self) -> str:
        """生成职位名称

        Returns:
            职位名称
        """
        return self.faker.job()

    # ==================== 复合数据生成 ====================

    def person_info(self, include_address: bool = True) -> Dict[str, Any]:
        """生成个人信息

        Args:
            include_address: 是否包含地址信息

        Returns:
            个人信息字典
        """
        person = {
            'name': self.chinese_name(),
            'age': random.randint(18, 65),
            'phone': self.phone_number(),
            'email': self.email(),
            'id_card': self.id_card(),
            'gender': random.choice(['男', '女'])
        }

        if include_address:
            person['address'] = self.chinese_address()
            person['province'] = self.province()
            person['city'] = self.city()

        return person

    def product_info(self) -> Dict[str, Any]:
        """生成产品信息

        Returns:
            产品信息字典
        """
        return {
            'product_id': self.order_number("PID", 6),
            'product_name': self.faker.word().capitalize() + " " + self.faker.word(),
            'price': round(random.uniform(10, 1000), 2),
            'category': random.choice(['电子产品', '服装', '食品', '家居', '运动']),
            'description': self.random_text(20, 50),
            'stock': random.randint(0, 1000)
        }

    def batch_person_info(self, count: int, include_address: bool = True) -> List[Dict[str, Any]]:
        """批量生成个人信息

        Args:
            count: 生成数量
            include_address: 是否包含地址信息

        Returns:
            个人信息列表
        """
        return [self.person_info(include_address) for _ in range(count)]

    # ==================== 特殊格式生成 ====================

    def credit_card(self) -> str:
        """生成信用卡号

        Returns:
            信用卡号
        """
        return self.faker.credit_card_number()

    def bank_account(self) -> str:
        """生成银行账号

        Returns:
            银行账号
        """
        return self.faker.iban()

    def ip_address(self) -> str:
        """生成IP地址

        Returns:
            IP地址
        """
        return self.faker.ipv4()

    def url(self) -> str:
        """生成URL

        Returns:
            URL地址
        """
        return self.faker.url()

    def password(self, length: int = 8, use_special: bool = True) -> str:
        """生成密码

        Args:
            length: 密码长度
            use_special: 是否包含特殊字符

        Returns:
            密码字符串
        """
        chars = string.ascii_letters + string.digits
        if use_special:
            chars += "!@#$%^&*"

        return ''.join(random.choices(chars, k=length))

    # ==================== 日期时间生成 ====================

    def random_date(self, start_year: int = 1990, end_year: int = 2025) -> str:
        """生成随机日期

        Args:
            start_year: 开始年份
            end_year: 结束年份

        Returns:
            随机日期字符串 (YYYY-MM-DD)
        """
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date(end_year, 12, 31)

        random_date = start_date + datetime.timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )

        return random_date.strftime("%Y-%m-%d")

    def random_datetime(self, start_year: int = 2020, end_year: int = 2025) -> str:
        """生成随机日期时间

        Args:
            start_year: 开始年份
            end_year: 结束年份

        Returns:
            随机日期时间字符串
        """
        return self.faker.date_time_between_dates(
            datetime.datetime(start_year, 1, 1),
            datetime.datetime(end_year, 12, 31)
        ).strftime("%Y-%m-%d %H:%M:%S")