"""
工具类使用示例

展示如何使用各种工具类进行常见操作
"""

from datetime import datetime
from src.utils import (
    DateTimeUtils,
    DataGenerator,
    StringUtils,
    FileUtils,
    NumberUtils
)


def datetime_examples():
    """时间工具使用示例"""
    print("=== 时间工具使用示例 ===")

    # 获取当前时间
    now = DateTimeUtils.now_str()
    print(f"当前时间: {now}")

    today = DateTimeUtils.today_str()
    print(f"今天日期: {today}")

    # 时间格式转换
    dt_str = "2023-12-25 15:30:45"
    dt_obj = DateTimeUtils.str_to_datetime(dt_str)
    print(f"字符串转datetime: {dt_obj}")

    # 时间计算
    diff = DateTimeUtils.get_time_diff("2023-01-01 10:00:00", "2023-12-31 20:00:00")
    print(f"时间差: {diff['days']}天 {diff['hours']}小时")

    # 时间加法
    new_time = DateTimeUtils.add_time("2023-12-25 10:00:00", days=7, hours=2)
    print(f"7天后2小时: {new_time}")

    # 年龄计算
    age = DateTimeUtils.get_age("1990-05-15")
    print(f"出生日期1990-05-15的年龄: {age}")

    # 工作日判断
    is_workday = DateTimeUtils.is_workday("2023-12-25")
    print(f"2023-12-25是工作日吗: {is_workday}")

    print()


def data_generator_examples():
    """数据生成工具使用示例"""
    print("=== 数据生成工具使用示例 ===")

    generator = DataGenerator()

    # 生成中文人名
    chinese_name = generator.chinese_name(gender='male')
    print(f"中文男性姓名: {chinese_name}")

    # 生成英文人名
    english_name = generator.english_name(gender='female')
    print(f"英文女性姓名: {english_name}")

    # 生成联系方式
    phone = generator.phone_number()
    email = generator.email(domain="company.com")
    print(f"手机号: {phone}")
    print(f"邮箱: {email}")

    # 生成地址信息
    address = generator.chinese_address()
    province = generator.province()
    city = generator.city()
    print(f"地址: {address}")
    print(f"省份: {province}")
    print(f"城市: {city}")

    # 生成身份证号
    id_card = generator.id_card()
    print(f"身份证号: {id_card}")

    # 生成产品信息
    product = generator.product_info()
    print(f"产品信息: {product}")

    # 批量生成人名
    names = generator.batch_chinese_names(5)
    print(f"批量生成的人名: {names}")

    print()


def string_utils_examples():
    """字符串处理工具使用示例"""
    print("=== 字符串处理工具使用示例 ===")

    text = "  Hello, 世界！这是一个测试文本。  "

    # 字符串清理
    cleaned = StringUtils.remove_extra_spaces(text)
    print(f"清理空格: '{cleaned}'")

    # 截断字符串
    truncated = StringUtils.truncate("这是一段很长的文本，需要被截断", 10)
    print(f"截断字符串: {truncated}")

    # 命名转换
    camel_case = "userName"
    snake_case = StringUtils.camel_to_snake(camel_case)
    print(f"驼峰转下划线: {camel_case} -> {snake_case}")

    # 提取信息
    chinese = StringUtils.extract_chinese("Hello世界123")
    numbers = StringUtils.extract_numbers("身高185cm，体重70kg")
    print(f"提取中文: {chinese}")
    print(f"提取数字: {numbers}")

    # 字符串验证
    is_valid_phone = StringUtils.is_valid_phone("13800138000")
    is_valid_email = StringUtils.is_valid_email("test@example.com")
    print(f"手机号验证: {is_valid_phone}")
    print(f"邮箱验证: {is_valid_email}")

    # 字符串加密
    md5_hash = StringUtils.md5_hash("hello world")
    print(f"MD5哈希: {md5_hash}")

    # 相似度比较
    similarity = StringUtils.similarity_ratio("hello", "helo")
    print(f"字符串相似度: {similarity}")

    print()


def file_utils_examples():
    """文件操作工具使用示例"""
    print("=== 文件操作工具使用示例 ===")

    # 文件大小格式化
    size_str = FileUtils.format_file_size(1024 * 1024 * 2.5)  # 2.5MB
    print(f"文件大小格式化: {size_str}")

    # 文件类型判断
    is_image = FileUtils.is_image_file("test.jpg")
    is_text = FileUtils.is_text_file("test.json")
    print(f"是图片文件: {is_image}")
    print(f"是文本文件: {is_text}")

    # 文件扩展名操作
    extension = FileUtils.get_file_extension("document.pdf")
    filename_without_ext = FileUtils.get_filename_without_extension("document.pdf")
    print(f"文件扩展名: {extension}")
    print(f"不含扩展名的文件名: {filename_without_ext}")

    # 目录操作
    dir_exists = FileUtils.ensure_dir("test_output")
    print(f"确保目录存在: {dir_exists}")

    # 文件读写示例（这里只是演示，实际文件不会被创建）
    content = "这是一些测试内容"
    # write_success = FileUtils.write_file("test.txt", content)
    # read_content = FileUtils.read_file("test.txt")
    print(f"要写入的内容: {content}")

    print()


def number_utils_examples():
    """数字处理工具使用示例"""
    print("=== 数字处理工具使用示例 ===")

    # 数字验证
    is_prime = NumberUtils.is_prime(17)
    is_even = NumberUtils.is_even(4)
    print(f"17是质数: {is_prime}")
    print(f"4是偶数: {is_even}")

    # 数字格式化
    formatted = NumberUtils.format_number(12345.6789, 2)
    percentage = NumberUtils.format_percentage(0.256, 1)
    currency = NumberUtils.format_currency(12345.67)
    print(f"数字格式化: {formatted}")
    print(f"百分比格式化: {percentage}")
    print(f"货币格式化: {currency}")

    # 数学计算
    average = NumberUtils.average([1, 2, 3, 4, 5])
    median = NumberUtils.median([1, 2, 3, 4, 5])
    variance = NumberUtils.variance([1, 2, 3, 4, 5])
    print(f"平均值: {average}")
    print(f"中位数: {median}")
    print(f"方差: {variance}")

    # 数值范围操作
    clamped = NumberUtils.clamp(150, 0, 100)
    normalized = NumberUtils.normalize(75, 0, 100)
    print(f"数值限制: {clamped}")
    print(f"归一化: {normalized}")

    # 特殊计算
    bmi = NumberUtils.calculate_bmi(70, 1.75)
    category = NumberUtils.calculate_bmi_category(bmi)
    print(f"BMI值: {bmi:.1f}")
    print(f"BMI分类: {category}")

    # 罗马数字转换
    roman = NumberUtils.int_to_roman(1999)
    number = NumberUtils.roman_to_int("MCMXCIX")
    print(f"1999的罗马数字: {roman}")
    print(f"MCMXCIX转换为数字: {number}")

    print()


def main():
    """主函数，运行所有示例"""
    print("🚀 工具类使用示例演示")
    print("=" * 50)

    # 运行各个示例
    datetime_examples()
    data_generator_examples()
    string_utils_examples()
    file_utils_examples()
    number_utils_examples()

    print("=" * 50)
    print("✅ 示例演示完成！")


if __name__ == "__main__":
    main()