# 工具类库

这是一个功能丰富的实用工具类库，提供了时间处理、数据生成、字符串处理、文件操作、数字处理等各种常用功能。

## 📁 文件结构

```
src/utils/
├── __init__.py           # 模块初始化文件
├── datetime_utils.py     # 时间处理工具类
├── data_generator.py     # 数据生成工具类
├── string_utils.py       # 字符串处理工具类
├── file_utils.py         # 文件操作工具类
├── number_utils.py       # 数字处理工具类
├── example_usage.py      # 使用示例
└── README.md            # 说明文档
```

## 🚀 快速开始

### 导入工具类

```python
from src.utils import (
    DateTimeUtils,
    DataGenerator,
    StringUtils,
    FileUtils,
    NumberUtils
)
```

## 📅 时间处理工具类 (DateTimeUtils)

### 基础功能
```python
# 获取当前时间
now = DateTimeUtils.now_str()  # "2023-12-25 15:30:45"
today = DateTimeUtils.today_str()  # "2023-12-25"

# 时间格式转换
dt = DateTimeUtils.str_to_datetime("2023-12-25 15:30:45")
time_str = DateTimeUtils.datetime_to_str(dt)
```

### 时间计算
```python
# 计算时间差
diff = DateTimeUtils.get_time_diff("2023-01-01", "2023-12-31")
# 返回: {'days': 364, 'hours': 0, 'minutes': 0, ...}

# 时间加法
new_time = DateTimeUtils.add_time("2023-12-25", days=7, hours=2)
# 返回: "2024-01-01 02:00:00"
```

### 高级功能
```python
# 年龄计算
age = DateTimeUtils.get_age("1990-05-15")  # 33

# 工作日判断
is_workday = DateTimeUtils.is_workday("2023-12-25")  # False

# 获取月份天数范围
start, end = DateTimeUtils.get_month_range(2023, 12)
# 返回: ("2023-12-01", "2023-12-31")
```

## 🎲 数据生成工具类 (DataGenerator)

### 人名生成
```python
generator = DataGenerator()

# 中文人名
chinese_name = generator.chinese_name(gender='male')  # 张三
english_name = generator.english_name(gender='female')  # Alice Smith

# 批量生成
names = generator.batch_chinese_names(10)
```

### 联系方式
```python
# 联系方式生成
phone = generator.phone_number()  # 13800138000
email = generator.email(domain="company.com")  # user@company.com
id_card = generator.id_card()  # 123456789012345678
```

### 地理信息
```python
# 地理信息生成
address = generator.chinese_address()  # 北京市朝阳区某某路123号
province = generator.province()  # 北京市
city = generator.city()  # 北京市
district = generator.district()  # 朝阳区
```

### 复合数据
```python
# 生成完整个人信息
person = generator.person_info(include_address=True)
# 返回: {'name': '张三', 'age': 25, 'phone': '...', 'address': '...'}

# 生成产品信息
product = generator.product_info()
# 返回: {'product_id': 'PID001', 'product_name': '...', 'price': 99.99}
```

## 🔤 字符串处理工具类 (StringUtils)

### 基础操作
```python
# 字符串检查和清理
is_empty = StringUtils.is_empty("  ")  # True
cleaned = StringUtils.remove_extra_spaces("  Hello  World  ")  # "Hello World"

# 字符串截断
truncated = StringUtils.truncate("这是一段很长的文本", 10)  # "这是一段..."
```

### 格式转换
```python
# 命名转换
camel = StringUtils.snake_to_camel("user_name")  # "userName"
snake = StringUtils.camel_to_snake("userName")  # "user_name"

# 格式化显示
phone = StringUtils.format_phone("13800138000")  # "138 0013 8000"
id_card = StringUtils.format_id_card("123456789012345678")  # "123456 789012345 678"
```

### 内容提取和验证
```python
# 内容提取
chinese = StringUtils.extract_chinese("Hello世界123")  # "世界"
numbers = StringUtils.extract_numbers("身高185cm")  # ["185"]

# 格式验证
is_phone = StringUtils.is_valid_phone("13800138000")  # True
is_email = StringUtils.is_valid_email("test@example.com")  # True
```

## 📁 文件操作工具类 (FileUtils)

### 文件信息
```python
# 文件信息获取
size = FileUtils.get_file_size("test.txt")  # 1024
size_str = FileUtils.format_file_size(1024*1024)  # "1.0 MB"
extension = FileUtils.get_file_extension("test.txt")  # "txt"

# 文件类型判断
is_image = FileUtils.is_image_file("photo.jpg")  # True
is_text = FileUtils.is_text_file("data.json")  # True
```

### 文件操作
```python
# 文件读写
content = FileUtils.read_file("test.txt")
success = FileUtils.write_file("output.txt", "Hello World")
success = FileUtils.append_file("log.txt", "New log entry")

# JSON和YAML操作
data = FileUtils.read_json_file("config.json")
success = FileUtils.write_json_file("config.json", {"key": "value"})
```

### 高级功能
```python
# 文件搜索
files = FileUtils.find_files_by_extension(".", [".txt", ".md"])
content_files = FileUtils.find_files_by_content(".", "关键词")

# 文件哈希
md5_hash = FileUtils.get_file_hash("file.txt", "md5")
```

## 🔢 数字处理工具类 (NumberUtils)

### 数字验证和判断
```python
# 数字验证
is_prime = NumberUtils.is_prime(17)  # True
is_even = NumberUtils.is_even(4)  # True

# 数字类型判断
is_positive = NumberUtils.is_positive_number("123")  # True
is_number = NumberUtils.is_number("3.14")  # True
```

### 数字格式化
```python
# 格式化显示
formatted = NumberUtils.format_number(12345.67, 2)  # "12,345.67"
percentage = NumberUtils.format_percentage(0.256, 1)  # "25.6%"
currency = NumberUtils.format_currency(1234.56)  # "¥1,234.56"
```

### 数学计算
```python
# 统计计算
average = NumberUtils.average([1, 2, 3, 4, 5])  # 3.0
median = NumberUtils.median([1, 2, 3, 4, 5])  # 3
variance = NumberUtils.variance([1, 2, 3, 4, 5])  # 2.0

# 数值范围
clamped = NumberUtils.clamp(150, 0, 100)  # 100
normalized = NumberUtils.normalize(75, 0, 100)  # 0.75
```

### 特殊计算
```python
# BMI计算
bmi = NumberUtils.calculate_bmi(70, 1.75)  # 22.86
category = NumberUtils.calculate_bmi_category(bmi)  # "正常"

# 罗马数字转换
roman = NumberUtils.int_to_roman(1999)  # "MCMXCIX"
number = NumberUtils.roman_to_int("MCMXCIX")  # 1999
```

## 🎯 使用示例

运行示例代码查看详细用法：

```python
python src/utils/example_usage.py
```

## 📋 依赖要求

部分功能需要额外依赖：

```bash
pip install faker  # 用于数据生成
pip install pyyaml  # 用于YAML文件操作
```

## 🔧 自定义配置

工具类支持自定义配置，例如：

```python
# 数据生成器支持不同语言环境
generator = DataGenerator(locale='en_US')

# 文件操作支持不同编码
content = FileUtils.read_file('file.txt', encoding='gbk')
```

## 🚨 注意事项

1. 文件操作前请确保有相应的读写权限
2. 数据生成工具主要用于测试和开发环境
3. 敏感信息处理时请注意数据隐私保护
4. 大文件操作时请注意内存使用情况

## 📞 支持与反馈

如有问题或建议，请联系开发团队。