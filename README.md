# UI+API 自动化+locust 性能测试框架

🚀 基于 Playwright、Pytest 和 OpenAPI 的 Web 应用 UI+API 自动化测试和 locust性能测试框架，支持智能 API 代码生成、数据库验证和丰富报告功能。

## 🌟 核心特性

### 🎯 测试能力

- **UI 自动化测试**: 基于 Playwright，支持主流浏览器
- **API 自动化测试**: 支持 REST API 全流程测试
- **智能 API 生成**: 从 OpenAPI 规范自动生成测试代码
- 支持以 locust 库的接口性能测试
- **数据库验证**: 支持 MySQL/SQLite 数据库操作
- **页面对象模式**: 封装页面元素，测试代码可读性强

### 🛠️ 技术特性

- **失败自动录制**: UI 测试失败时自动截图和录制视频
- **智能断言失败信息**: 中文化断言失败描述
- **日志系统**: 结构化日志记录，自动按天分割
- **并行测试执行**: 支持并发测试提高效率
- **Allure 报告**: 丰富的测试报告和数据可视化

### 📊 报告功能

- 详细的测试步骤记录
- 失败时自动附加截图和视频
- 测试执行时间统计
- 历史趋势分析和对比

## 📁 项目结构

```
web-app-terminal-auto-test/
├── src/                          # 源代码目录
│   ├── core/                     # 核心工具模块
│   │   ├── db_client.py          # 数据库客户端（MySQL/SQLite）
│   │   ├── http_client.py        # HTTP 客户端，支持自动登录
│   │   ├── http_response.py      # HTTP 响应处理器
│   │   ├── gen_apis.py           # API 代码生成器
│   │   ├── data/                 # 数据管理
│   │   │   ├── apis.db           # SQLite 数据库文件
│   │   │   ├── gen_api_db.py     # API 数据管理器
│   │   │   └── models.py         # 数据模型
│   │   └── openapi/              # OpenAPI 规范
│   │       └── openapi.json      # OpenAPI 3.0 规范文件
│   └── pages/                    # 页面对象模型
│       ├── __init__.py
│       ├── base_page.py          # 基础页面类
│       ├── login.py              # 登录页面类
│       └── user.py               # 用户管理页面类
├── tests/                        # 测试用例目录
│   ├── api/                      # API 测试用例
│   │   └── test_user.py          # 用户 API 测试
│   └── ui/                       # UI 测试用例
│       └── test_user_ui.py       # 用户 UI 测试
├── logs/                         # 日志文件目录
├── reports/                      # 测试报告目录
│   ├── allure-results/           # Allure 原始结果
│   ├── html/                     # HTML 报告
│   ├── screenshots/              # 测试截图
│   └── videos/                   # 测试视频录制
├── conftest.py                   # pytest 配置文件
├── pytest.ini                    # pytest 设置
├── settings.py                   # 项目配置
├── run_tests.py                  # 测试运行脚本
├── requirements.txt              # 依赖包列表
└── README.md                     # 项目文档
```

## 🛠️ 技术栈

| 组件                 | 版本   | 说明          |
| -------------------- | ------ | ------------- |
| **Python**     | 3.8+   | 编程语言      |
| **Playwright** | 1.55.0 | UI 自动化测试 |
| **Pytest**     | 8.4.2  | 测试框架      |
| **Allure**     | 2.15.0 | 测试报告框架  |
| **Requests**   | 2.32.5 | HTTP 客户端   |
| **PyMySQL**    | 1.1.2  | MySQL 驱动    |
| **Loguru**     | 0.7.3  | 日志记录库    |
| **SQLAlchemy** | 1.4.54 | 数据库 ORM    |
| **Jinja2**     | 3.1.6  | 模板引擎      |
| **DBUtils**    | 3.1.2  | 数据库连接池  |

## ⚡ 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd auto-test

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install

# 安装 Allure 报告工具 (需要 Java 8+ 环境)
# 注意: Allure 需要 Java 环境才能运行，请先确保安装了 Java

# 安装 Java (Allure 依赖)
# macOS
brew install openjdk@11
echo 'export PATH="/usr/local/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
# 或在新版本 macOS 上
brew install openjdk@21

# Windows
# 下载并安装 JDK: https://adoptium.net/
# 或使用 Chocolatey: choco install openjdk
# 设置 JAVA_HOME 环境变量

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# 安装 Allure
# macOS
brew install allure

# Windows
# 方式1: 使用 Scoop (推荐)
scoop install allure
# 方式2: 下载安装包
# 从 https://github.com/allure-framework/allure2/releases 下载 allure-x.x.x.zip
# 解压后将 bin 目录添加到系统 PATH 环境变量

# Linux (Ubuntu/Debian)
# 方式1: 使用包管理器
sudo apt install allure
# 方式2: 下载二进制包
# 从 https://github.com/allure-framework/allure2/releases 下载对应版本
# 解压后将 bin 目录添加到 PATH 环境变量

# 验证安装
java -version
allure --version
```

### 2. 配置数据库

编辑 `settings.py` 文件中的数据库配置：

```python
class DB:
    """数据库配置"""

    class fastapi_admin:
        host = "localhost"
        port = 3306
        user = "your_username"
        password = "your_password"
        database = "fastapi_admin"
        charset = "utf8"

    class your_db:
        # 更多数据库配置...
        pass
```

### 3. 配置测试环境

在 `settings.py` 中配置测试环境：

```python
class ENV:
    # 测试环境
    test = 'http://localhost:3100'

    # 生产环境
    online = 'https://your-app.com'

class ACCOUNT:
    admin = {'username': 'admin', 'password': '123456'}
    test_user = {'username': 'test', 'password': '123456'}
```

## 🚀 运行测试

### 使用 run_tests.py 脚本

```bash
# 运行所有测试
python run_tests.py

# 只运行 UI 测试
python run_tests.py --ui

# 只运行 API 测试
python run_tests.py --api

# 运行冒烟测试
python run_tests.py --smoke

# 指定浏览器（chromium/firefox/webkit）
python run_tests.py --browser firefox

# 并行运行测试
python run_tests.py --parallel 4
```

### 直接使用 pytest 命令

```bash
# 运行所有测试
pytest

# 运行 UI 测试
pytest -m ui

# 运行 API 测试
pytest -m api

# 生成并打开报告
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### 高级运行选项

```bash
# 并行测试执行
pytest -n 4

# 指定浏览器
pytest --browser chromium

# 显示详细输出
pytest -v

# 重新运行失败的测试
pytest --rerunfailures=3
```

## 🤖 智能 API 生成

### 导入 API 规范

1. 将 OpenAPI 3.0 JSON 文件放置到 `src/core/openapi/openapi.json`
2. 运行 API 代码生成：

```bash
# 生成 API 测试代码
python -m src.core.gen_apis
```

3. 自动生成的文件：
   - `src/apis/api_mixin1.py` (根据 API 数量可能生成多个文件)
   - `src/apis/__init__.py`

### 使用生成的 API

```python
from src.core.http_client import HttpClient
from settings import ENV, ACCOUNT

# 创建 HTTP 客户端
client = HttpClient(ENV.test, **ACCOUNT.admin)

# 使用自动生成的 API 方法
# 示例：获取用户信息
user_info = client.api_v1_user_profile_g(user_id=123)
print(user_info.json())

# 示例：创建用户信息
new_user = client.api_v1_user_create_p(
    username='testuser',
    password='123456',
    email='test@example.com',
    is_active=True
)
```

## 📝 编写测试用例

### UI 测试用例

```python
import pytest
import allure
from playwright.sync_api import Page
from src.pages.login import LoginPage
from src.pages.user import UserPage

@allure.feature("用户管理")
class TestUserManagement:

    @allure.title("用户登录功能")
    @pytest.mark.ui
    def test_user_login(self, page: Page):
        """测试用户登录"""
        with allure.step("访问登录页面"):
            login_page = LoginPage(page)
            login_page.navigate()

        with allure.step("执行登录操作"):
            login_page.login("admin", "123456")

        with allure.step("验证登录成功"):
            assert login_page.is_logged_in()

    @allure.title("添加新用户")
    @pytest.mark.ui
    def test_create_user(self, page: Page):
        """测试添加新用户"""
        # 登录步骤（可以提取到 fixture 中复用）
        login_page = LoginPage(page)
        login_page.login("admin", "123456")

        # 用户管理
        user_page = UserPage(page)
        user_page.create_user({
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '123456'
        })

        # 验证创建成功
        assert user_page.user_exists("testuser")
```

### API 测试用例

```python
import pytest
import allure
from src.core.http_client import HttpClient
from settings import ENV, ACCOUNT

@allure.feature("用户API")
class TestUserAPI:

    def setup_method(self):
        """测试前准备"""
        self.client = HttpClient(ENV.test, **ACCOUNT.admin)

    @allure.title("获取用户列表")
    @pytest.mark.api
    def test_get_user_list(self):
        """测试获取用户列表"""
        response = self.client.api_v1_user_list_g()

        with allure.step("验证响应状态"):
            assert response.status_code == 200

        with allure.step("验证数据结构"):
            data = response.json()
            assert "data" in data
            assert isinstance(data["data"], list)

    @allure.title("创建用户")
    @pytest.mark.api
    def test_create_user(self):
        """测试创建用户"""
        user_data = {
            'username': 'testuser',
            'password': '123456',
            'email': 'test@example.com'
        }

        response = self.client.api_v1_user_create_p(**user_data)

        # 验证创建成功
        assert response.status_code == 200
        assert response.search('msg') == 'OK'

        # 验证数据插入到数据库
        db_user = self.client.db.fastapi_admin.select(
            table='user',
            condition=f"username='{user_data['username']}'"
        )
        assert len(db_user) > 0
```

### 数据库验证示例

```python
import pytest
from src.core.db_client import MysqlClient

class TestDatabaseOperations:

    def test_database_crud(self):
        """测试数据库 CRUD 操作"""
        db_client = MysqlClient({
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'database': 'test_db'
        })

        # 插入数据
        db_client.insert('test_table', 'name,age', ('John', 25))

        # 查询数据
        result = db_client.select('test_table', 'name="John"')
        assert len(result) > 0
        assert result[0]['age'] == 25

        # 更新数据
        db_client.update('test_table', 'name="John"', 'age=30')

        # 删除数据
        db_client.delete('test_table', 'name="John"')
```

## 📊 测试报告

### 查看 Allure 报告

```bash
# 生成 HTML 报告
allure generate reports/allure-results -o reports/html --clean

# 启动 Allure 服务器（推荐）
allure serve reports/allure-results
```

### 报告功能

- ✅ **测试步骤详情**: 每个步骤的执行状态和时间
- ✅ **失败媒体附件**: 截图、视频自动附加到失败用例
- ✅ **统计信息**: 通过/失败比率，执行时间
- ✅ **历史对比**: 趋势图和历史数据分析
- ✅ **环境信息**: 测试环境配置和系统信息

## 🏗️ 架构说明

### HTTP 客户端架构

```
HttpClient (继承 RequestsPro + AllApiMixin)
├── auto_login(): 自动登录和 Token 管理
├── db: 数据库操作客户端
├── sqlite_db: SQLite 本地缓存
└── api_xxx(): 动态生成的 API 方法
```

### 数据库连接架构

```
Database Clients
├── MysqlClient: MySQL 连接池 + CRUD 操作
└── SqliteClient: SQLite 文件数据库操作
```

### 测试执行流程

```
Test Execution Flow
├── conftest.py: 环境配置和 fixture
├── pytest.ini: 测试标记和配置
├── run_tests.py: 智能测试运行脚本
└── reports/: 生成测试报告和媒体文件
```

## 🔧 配置和定制

### pytest.ini 配置

```ini
[pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts =
    --tb=short
    --strict-markers
    --alluredir=reports/allure-results
    --browser chromium
markers =
    ui: Web UI 自动化测试
    api: API 接口测试
    smoke: 冒烟测试
    regression: 回归测试
```

### Loguru 日志配置

查看 `conftest.py` 中的日志配置，支持：

- 按天自动分割日志文件
- 结构化 JSON 格式
- 控制台和文件双输出

## 🚀 最佳实践

### 1. 页面对象模式

- 为每个页面创建专门的 Page 类
- 将页面元素定位和操作封装在 Page 类中
- 使用链式调用提高代码可读性

### 2. 测试数据管理

- 使用 fixture 管理复杂的测试数据
- 测试完成后自动清理数据
- 避免测试用例之间的数据依赖

### 3. API 测试策略

- 优先使用生成的 API 方法
- 关键功能点进行数据库验证
- 结合 UI 操作验证业务流程

### 4. 失败处理

- 编写有意义的断言信息
- 利用自动截图定位问题
- 通过日志跟踪执行过程

## 🐛 故障排除

### 常见问题

1. **Playwright 浏览器安装失败**

   ```bash
   playwright install --with-deps
   ```
2. **数据库连接失败**

   - 检查数据库服务状态
   - 验证连接参数配置
   - 确认用户权限设置
3. **API 调用失败**

   - 检查自动登录状态
   - 验证 Token 缓存有效性
   - 确认 API 规范和参数匹配
4. **报告生成失败**

   - 确保 Allure 命令已安装
   - 检查报告目录权限
   - 清理旧的 results 文件

### 调试技巧

```bash
# 开启调试模式
pytest --pdb -s

# 查看详细日志
pytest -v

# 只运行失败用例
pytest --lf

# 显示所有输出
pytest --capture=no
```

**🚀 快速开始:**`python run_tests.py --smoke`

**📊 查看报告:** `allure serve reports/allure-results`

**🔧 调试测试:** `python run_tests.py --verbose`

## 🔒 许可证

本项目为内部闭源项目，仅限于授权用户使用。

---

## 📞 联系方式

如有技术问题或使用指导，请联系作者。

**[🔙 返回顶部](#webapp-terminal-测试自动化框架)**
