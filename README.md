# UI + API 自动化测试框架

基于 **Playwright + Pytest + OpenAPI** 的 Web 应用自动化测试框架，集成 UI 测试、API 测试、数据库校验和 Locust 性能测试，支持 Allure 报告和 Jenkins CI。

## 核心特性

- **UI 自动化** — 基于 Playwright，支持 Chromium / Firefox / WebKit，页面对象模式封装
- **API 自动化** — 从 OpenAPI 3.0 规范自动生成 API 调用方法，无需手写 HTTP 请求
- **数据库校验** — 支持 MySQL（连接池）和 SQLite，API 操作后直接查库验证
- **失败自动录制** — 测试失败自动截图 + 录屏，附加到 Allure 报告
- **中文化断言** — 自定义断言失败消息，中文展示差异对比
- **CI 就绪** — Docker 镜像 + Jenkins Pipeline + 企业微信通知

## 项目结构

```
auto-test/
├── src/
│   ├── core/
│   │   ├── db_client.py          # MysqlClient / SqliteClient
│   │   ├── http_client.py        # HttpClient（自动登录 + API 调用）
│   │   ├── http_response.py      # 响应处理（JMESPath 提取 + 正则匹配）
│   │   ├── gen_apis.py           # 从 OpenAPI 生成 API 代码
│   │   ├── data/                 # SQLite ORM 模型和 API 缓存
│   │   ├── openapi/              # OpenAPI 3.0 规范文件
│   │   └── tpl/                  # Jinja2 代码生成模板
│   ├── pages/
│   │   ├── base_page.py          # Playwright 页面基类
│   │   ├── login.py              # 登录页面对象
│   │   └── user.py               # 用户管理页面对象
│   ├── apis/                     # 自动生成的 API mixin 类
│   └── utils/                    # 工具库（数据生成、日期、字符串、文件等）
├── tests/
│   ├── api/test_user.py          # 用户 API 测试
│   └── ui/test_user_ui.py        # 用户 UI 测试
├── performance/
│   └── user_per.py               # Locust 性能测试
├── conftest.py                   # Pytest fixtures、hooks、日志配置
├── settings.py                   # 项目配置（环境、账号、数据库）
├── run_tests.py                  # 测试执行入口
├── pytest.ini                    # Pytest 标记和默认参数
├── requirements.txt              # 依赖包（锁定版本）
├── Dockerfile                    # CI 镜像
├── Jenkinsfile                   # Jenkins 流水线
└── README.md / README_EN.md      # 文档
```

## 快速开始

### 1. 环境准备

```bash
cd auto-test

# 创建虚拟环境
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### 2. 安装 Allure（查看报告需要）

Allure CLI 依赖 Java，请先确保安装了 JDK 8+：

```bash
# macOS
brew install openjdk@11 allure

# Windows (推荐 Scoop)
scoop install allure

# Linux
sudo apt install openjdk-11-jdk allure
```

验证安装：

```bash
java -version
allure --version
```

### 3. 配置

编辑 `settings.py`：

```python
# 测试目标地址
class ENV:
    test = 'http://localhost:3100'
    online = 'https://your-app.com'

# 测试账号
class ACCOUNT:
    admin = {'username': 'admin', 'password': '123456'}

# 数据库
class DB:
    class fastapi_admin:
        host = "localhost"
        port = 3306
        user = "root"
        password = "your_password"
        database = "fastapi_admin"
        charset = "utf8"
```

也可以通过环境变量动态覆盖配置，无需修改代码：

| 环境变量 | 说明 | 默认值 |
|---|---|---|
| `TARGET_ENV` | 选择环境 `test` / `online` | `test` |
| `BASE_URL` | 应用地址 | 取自 `ENV` 类 |
| `DB_HOST` | MySQL 主机 | `localhost` |
| `DB_PORT` | MySQL 端口 | `3306` |
| `DB_USER` | MySQL 用户 | `fastapi_admin` |
| `DB_PASSWORD` | MySQL 密码 | `fastapi_admin_password` |
| `DB_NAME` | MySQL 库名 | `fastapi_admin` |

## 运行测试

### run_tests.py（推荐）

封装了 目录创建 → 执行测试 → 解析结果 → 生成报告 → 企微通知 的完整流程：

```bash
# 运行全部测试并生成报告
python run_tests.py

# 只跑冒烟测试
python run_tests.py --smoke

# 只跑 API 测试
python run_tests.py --api

# 只跑 UI 测试
python run_tests.py --ui

# 指定浏览器
python run_tests.py --browser firefox

# 并行执行（4 个 worker）
python run_tests.py --parallel 4

# 详细输出
python run_tests.py --verbose
```

### 直接使用 Pytest

```bash
# 全部测试
pytest

# 按标记筛选
pytest -m api
pytest -m ui
pytest -m smoke

# 生成 Allure 结果并查看
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# 并行执行
pytest -n 4

# 失败重跑
pytest --rerunfailures=3
```

### Pytest 标记

| 标记 | 说明 |
|---|---|
| `api` | API 接口测试 |
| `ui` | Playwright UI 测试 |
| `smoke` | 冒烟测试 |
| `regression` | 回归测试 |

## 自动生成 API 方法

框架可以从 OpenAPI 3.0 规范自动生成 Python API 调用代码，无需手动写 HTTP 请求。

**操作步骤：**

1. 将 OpenAPI 3.0 JSON 文件放到 `src/core/openapi/openapi.json`
2. 运行生成器：

```bash
python -m src.core.gen_apis
```

3. 生成的文件会出现在 `src/apis/` 目录下（如 `api_mixin1.py`）

**使用示例：**

```python
from src.core.http_client import HttpClient
from settings import env, account

# HttpClient 会自动登录并缓存 Token
client = HttpClient(env.base_url, **account.admin)

# 调用自动生成的方法（命名规则：api_{路径}_{HTTP方法}）
users = client.api_v1_user_list_g()
print(users.json())

new_user = client.api_v1_user_create_p(
    username='testuser', password='123456', email='test@example.com'
)
```

## 编写测试用例

### API 测试

```python
import allure
import pytest
from src.core.http_client import HttpClient
from settings import env, account

@allure.feature("用户管理")
class TestUserAPI:

    def setup_method(self):
        self.client = HttpClient(env.base_url, **account.admin)

    @allure.title("创建用户并验证数据库写入")
    @pytest.mark.api
    def test_create_user(self):
        response = self.client.api_v1_user_create_p(
            username='testuser', password='123456', email='test@example.com'
        )
        assert response.status_code == 200

        # 查数据库验证数据确实写入
        db_result = self.client.db.fastapi_admin.select(
            table='user', condition="username='testuser'"
        )
        assert len(db_result) > 0
```

### UI 测试

```python
import allure
import pytest
from src.pages.login import LoginPage
from src.pages.user import UserPage

@allure.feature("用户管理")
class TestUserUI:

    @allure.title("通过 UI 添加用户")
    @pytest.mark.ui
    def test_add_user(self, login_page: LoginPage, user_page: UserPage):
        with allure.step("创建用户"):
            user_page.add_user(username='testuser', email='test@example.com')

        with allure.step("验证列表中可见"):
            assert user_page.user_exists('testuser')
```

### 数据库操作

```python
from src.core.db_client import MysqlClient

db = MysqlClient({
    'host': 'localhost', 'port': 3306,
    'user': 'root', 'password': 'pwd', 'database': 'mydb'
})

db.insert('users', 'name,age', ('Alice', 30))
results = db.select('users', "name='Alice'")
db.update('users', "name='Alice'", 'age=31')
db.delete('users', "name='Alice'")
```

## 查看测试报告

```bash
# 启动 Allure 服务（自动打开浏览器）
allure serve reports/allure-results

# 生成静态 HTML
allure generate reports/allure-results -o reports/html --clean
```

报告包含：
- 每个步骤的执行状态和耗时
- 失败用例自动附带的截图和视频
- 通过率统计和历史趋势图
- 测试环境信息

## CI/CD 集成

### Docker 运行

```bash
# 构建镜像
docker build -t auto-test .

# 运行测试
docker run --rm \
  -e TARGET_ENV=test \
  -e BASE_URL=http://host.docker.internal:3100 \
  -e DB_HOST=host.docker.internal \
  auto-test python run_tests.py
```

### Jenkins Pipeline

项目自带 `Jenkinsfile`，包含两个阶段：
1. **Run Tests** — 在 Docker 容器内执行 `python run_tests.py`
2. **Generate Allure Report** — 使用 Jenkins Allure 插件生成 HTML 报告

配置参数 `TARGET_ENV`（`test` / `online`）即可切换环境。测试结束后自动发送企业微信通知（含通过率和报告链接）。详见 `JENKINS_CI_GUIDE.md`。

## 架构概览

```
HttpClient（继承 AllApiMixin）
├── auto_login()      →  自动登录，Token 缓存到本地 SQLite
├── db                →  MysqlClient，用于后端数据校验
├── sqlite_db         →  SqliteClient，本地缓存
└── api_xxx()         →  自动生成的 API 方法

测试执行流程
conftest.py（fixtures、日志、截图录屏 hooks）
  → pytest 执行 cases（按标记筛选）
  → run_tests.py 解析结果、生成 Allure 报告
  → 企微通知（通过率 + 报告链接）
```

## 常见问题

| 问题 | 解决方法 |
|---|---|
| 浏览器未安装 | `playwright install --with-deps` |
| 数据库连接失败 | 检查 `settings.py` 中 DB 配置，确认数据库服务已启动 |
| Allure 命令找不到 | `brew install allure` (macOS) / `scoop install allure` (Windows) / `apt install allure` (Linux) |
| Allure 提示缺少 Java | 安装 JDK 8+：`brew install openjdk@11` (macOS) |
| API 返回 401 | 检查 `settings.py` 中 ACCOUNT 账号密码，确认 Token 缓存有效 |
| 截图/视频未生成 | 确认 `reports/screenshots/` 和 `reports/videos/` 目录存在 |

## License

MIT
