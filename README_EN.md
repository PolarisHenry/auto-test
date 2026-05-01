# UI + API Automation Testing Framework

A Playwright + Pytest + OpenAPI based hybrid test framework supporting UI automation, API testing, database verification, and Locust performance testing.

## Features

- **UI Testing** — Playwright with Chromium/Firefox/WebKit, Page Object pattern
- **API Testing** — auto‑generated API methods from OpenAPI 3.0 specs
- **Database Verification** — MySQL (connection pool) + SQLite backends
- **Performance Testing** — Locust‑based load tests
- **Rich Reporting** — Allure reports with screenshots and video on failure
- **CI Ready** — Docker image + Jenkins pipeline + WeChat Work notifications

## Project Structure

```
auto-test/
├── src/
│   ├── core/
│   │   ├── db_client.py          # MysqlClient + SqliteClient
│   │   ├── http_client.py        # HttpClient (auto‑login, API calls)
│   │   ├── http_response.py      # JMESPath + regex response helpers
│   │   ├── gen_apis.py           # API code generator from OpenAPI
│   │   ├── data/                 # SQLite ORM models & manager
│   │   ├── openapi/              # OpenAPI 3.0 spec files
│   │   └── tpl/                  # Jinja2 templates for code gen
│   ├── pages/
│   │   ├── base_page.py          # Playwright base page class
│   │   ├── login.py              # Login page object
│   │   └── user.py               # User management page object
│   ├── apis/                     # Auto‑generated API mixin classes
│   └── utils/                    # Data generator, string, file, date utils
├── tests/
│   ├── api/test_user.py          # User API test cases
│   └── ui/test_user_ui.py        # User UI test cases
├── performance/
│   └── user_per.py               # Locust performance test
├── conftest.py                   # Pytest fixtures, hooks, logging
├── settings.py                   # Central configuration
├── run_tests.py                  # Test runner entry point
├── pytest.ini                    # Pytest markers and defaults
├── requirements.txt              # Dependencies (pinned versions)
├── Dockerfile                    # Docker image for CI
├── Jenkinsfile                   # Jenkins declarative pipeline
└── README.md / README_EN.md      # Documentation
```

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Java 8+ (for Allure CLI)

### 2. Install Dependencies

```bash
cd auto-test

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 3. Configure

Edit `settings.py` with your environment details:

```python
# Target app URL
class ENV:
    test = 'http://localhost:3100'
    online = 'https://your-app.com'

# Test account
class ACCOUNT:
    admin = {'username': 'admin', 'password': '123456'}

# Database
class DB:
    class fastapi_admin:
        host = "localhost"
        port = 3306
        user = "root"
        password = "your_password"
        database = "fastapi_admin"
        charset = "utf8"
```

Configuration can also be overridden via environment variables:

| Variable | Purpose | Default |
|---|---|---|
| `TARGET_ENV` | Which environment to use (`test` / `online`) | `test` |
| `BASE_URL` | App base URL | from `ENV` class |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `fastapi_admin` |
| `DB_PASSWORD` | MySQL password | `fastapi_admin_password` |
| `DB_NAME` | MySQL database | `fastapi_admin` |

## Running Tests

### Using run_tests.py (recommended)

```bash
# Run all tests with report generation
python run_tests.py

# Run only smoke tests
python run_tests.py --smoke

# Run API tests only
python run_tests.py --api

# Run UI tests only
python run_tests.py --ui

# Run with a specific browser
python run_tests.py --browser firefox

# Run in parallel (n workers)
python run_tests.py --parallel 4

# Verbose output
python run_tests.py --verbose
```

`run_tests.py` handles: directory setup → test execution → result parsing → Allure report generation → optional WeChat Work notification.

### Using Pytest Directly

```bash
# All tests
pytest

# By marker
pytest -m api
pytest -m ui
pytest -m smoke

# With Allure
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# Parallel
pytest -n 4

# Retry failures
pytest --rerunfailures=3
```

### Markers

| Marker | Description |
|---|---|
| `api` | API / endpoint tests |
| `ui` | Playwright browser tests |
| `smoke` | Smoke test subset |
| `regression` | Full regression suite |

## Auto‑Generating API Methods

1. Place your OpenAPI 3.0 JSON file at `src/core/openapi/openapi.json`
2. Run the generator:

```bash
python -m src.core.gen_apis
```

3. Generated files appear under `src/apis/` (e.g., `api_mixin1.py`).

Use the generated methods with `HttpClient`:

```python
from src.core.http_client import HttpClient
from settings import env, account

client = HttpClient(env.base_url, **account.admin)
response = client.api_v1_user_list_g()
print(response.json())
```

## Writing Tests

### API Test Example

```python
import allure
import pytest
from src.core.http_client import HttpClient
from settings import env, account

@allure.feature("User Management")
class TestUserAPI:

    def setup_method(self):
        self.client = HttpClient(env.base_url, **account.admin)

    @allure.title("Create a user")
    @pytest.mark.api
    def test_create_user(self):
        response = self.client.api_v1_user_create_p(
            username='testuser', password='123456', email='test@example.com'
        )
        assert response.status_code == 200

        # Verify in database
        db_user = self.client.db.fastapi_admin.select(
            table='user', condition="username='testuser'"
        )
        assert len(db_user) > 0
```

### UI Test Example

```python
import allure
import pytest
from playwright.sync_api import Page
from src.pages.login import LoginPage
from src.pages.user import UserPage

@allure.feature("User Management")
class TestUserUI:

    @allure.title("Add user via UI")
    @pytest.mark.ui
    def test_add_user(self, login_page: LoginPage, user_page: UserPage):
        with allure.step("Create user"):
            user_page.add_user(username='testuser', email='test@example.com')

        with allure.step("Verify user appears in list"):
            assert user_page.user_exists('testuser')
```

### Database Verification

```python
from src.core.db_client import MysqlClient

db = MysqlClient({
    'host': 'localhost', 'port': 3306,
    'user': 'root', 'password': 'pwd', 'database': 'mydb'
})

# CRUD operations
db.insert('users', 'name,age', ('Alice', 30))
results = db.select('users', "name='Alice'")
db.update('users', "name='Alice'", 'age=31')
db.delete('users', "name='Alice'")
```

## Viewing Reports

```bash
# Open Allure report in browser
allure serve reports/allure-results

# Generate static HTML
allure generate reports/allure-results -o reports/html --clean
```

Reports include:
- Step‑by‑step execution details
- Screenshots and videos attached to failed tests
- Pass/fail statistics and duration
- Historical trend charts (Allure history)

## CI / CD (Jenkins + Docker)

The project includes a Dockerfile and Jenkinsfile for out‑of‑box CI integration:

```bash
# Build Docker image
docker build -t auto-test .

# Run inside Docker
docker run --rm \
  -e TARGET_ENV=test \
  -e BASE_URL=http://host.docker.internal:3100 \
  -e DB_HOST=host.docker.internal \
  auto-test python run_tests.py
```

### Jenkins Pipeline

- **Parameter**: `TARGET_ENV` — choose `test` or `online`
- **Stage 1**: Run tests inside the Docker container
- **Stage 2**: Generate Allure HTML report
- **Post**: Sends WeChat Work notification with pass‑rate summary and report link

See `JENKINS_CI_GUIDE.md` for detailed setup instructions.

## Architecture

```
HttpClient (extends AllApiMixin)
├── auto_login()       →  automatic token acquisition & refresh
├── db                 →  MysqlClient for backend verification
├── sqlite_db          →  SqliteClient for local caching
└── api_xxx()          →  auto‑generated API methods

Test Flow
├── conftest.py        →  fixtures, logging, screenshot/video hooks
├── pytest.ini         →  markers and default options
├── run_tests.py       →  orchestration & reporting
└── reports/           →  Allure results, HTML, screenshots, videos
```

## Troubleshooting

| Problem | Solution |
|---|---|
| Playwright browser missing | `playwright install --with-deps` |
| DB connection refused | Check DB host/port, verify service is running |
| Allure command not found | Install via `brew install allure` (macOS), `scoop install allure` (Windows), or `apt install allure` (Linux) |
| Allure requires Java | Install JDK 8+ — `brew install openjdk@11` (macOS) |
| API call returns 401 | Check `ACCOUNT` credentials in `settings.py`, verify token cache |
| Screenshot/video missing | Check `reports/screenshots/` and `reports/videos/` directories exist |

## License

MIT
