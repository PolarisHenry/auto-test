# Jenkins 自动化测试 CI 实践指南

## 整体流程

```
代码 push 到 GitHub
       ↓
Jenkins 拉取代码
       ↓
安装 Python 依赖 + Playwright 浏览器
       ↓
启动后端服务 + MySQL（或指向已运行的服务）
       ↓
运行 pytest 自动化测试
       ↓
生成 Allure 报告 → Jenkins 页面直接查看
```

---

## 1. 确认 Jenkins 容器状态

```bash
# 查看当前 Jenkins 容器
docker ps | grep jenkins
```

### 如果 Jenkins 容器还未创建，推荐用以下命令创建：

```bash
docker run -d \
  --name jenkins \
  --add-host=host.docker.internal:host-gateway \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

关键参数说明：

| 参数                                             | 作用                                                                                                |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `--add-host=host.docker.internal:host-gateway` | Jenkins 容器可通过 `host.docker.internal` 访问宿主机上的服务（如 3100 端口的后端、3306 的 MySQL） |
| `-v /var/run/docker.sock:/var/run/docker.sock` | 让 Jenkins 内部可以调用宿主机 Docker（在 pipeline 里启动 MySQL 等容器）                             |
| `-p 8080:8080`                                 | Jenkins Web 界面端口                                                                                |

### 验证 Jenkins 能访问宿主机：

```bash
docker exec -it jenkins bash
curl http://host.docker.internal:3100
```

---

## 2. 修改 settings.py 支持环境变量覆盖

当前 `settings.py` 硬编码了 `localhost:3100`，Jenkins 容器内无法通过 `localhost` 访问宿主机。

修改 `auto_test/settings.py`：

```python
import os
from pathlib import Path

from src.core.db_client import MysqlClient

ROOT_PATH = Path(__file__).parent

API_DB_PATH = ROOT_PATH / 'src/core/data/apis.db'
OPENPAI_PATH = ROOT_PATH / 'src/core/openapi'
OPENPAI_URLS = {
    'openapi': 'http://localhost:3100/openapi.json',
}

WECOM_WEBHOOK: str = os.environ.get(
    'WECOM_WEBHOOK',
    'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx'
)


class ENV:
    test = os.environ.get('BASE_URL', 'http://localhost:3100')
    online = os.environ.get('BASE_URL', 'http://localhost:3100')


class ACCOUNT:
    admin = {'username': 'admin', 'password': '123456'}


class DB:
    __COMMON_DB_CONFIG = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', '3306')),
        'user': os.environ.get('DB_USER', 'fastapi_admin'),
        'password': os.environ.get('DB_PASSWORD', 'fastapi_admin_password'),
        'charset': 'utf8',
    }

    fastapi_admin: dict | MysqlClient = {
        **__COMMON_DB_CONFIG,
        'database': os.environ.get('DB_NAME', 'fastapi_admin'),
    }


env = ENV()
account = ACCOUNT()

if __name__ == '__main__':
    print(DB.fastapi_admin)
```

本地运行行为不变（默认值都是 `localhost`），CI 中通过环境变量覆盖。

---

## 3. Jenkins 安装必要的插件

打开 Jenkins → Manage Jenkins → Plugins → Available plugins，搜索安装：

| 插件                      | 用途                                    |
| ------------------------- | --------------------------------------- |
| **Allure**          | 在 Jenkins 页面展示 Allure 测试报告     |
| **JUnit**           | 展示 JUnit 测试趋势图（通常自带）       |
| **Docker Pipeline** | 在 pipeline 里管理容器（启动 MySQL 等） |
| **Pipeline**        | Pipeline as Code 支持（通常自带）       |

---

## 4. 配置 Allure 全局工具

Manage Jenkins → Tools → Allure Commandline → Add Allure：

- Name: `allure`
- 勾选 "Install automatically"
- 版本选择最新的 `2.33.0`

![Allure 配置](https://i.imgur.com/placeholder.png)

---

## 5. 创建 Jenkinsfile

在项目根目录（`/web-app-teminal/`）创建 `Jenkinsfile`：

```groovy
pipeline {
    agent any

    environment {
        // Jenkins 容器内通过 host.docker.internal 访问宿主机
        BASE_URL       = 'http://host.docker.internal:3100'
        DB_HOST        = 'host.docker.internal'
        DB_PORT        = '3306'
        DB_USER        = 'fastapi_admin'
        DB_PASSWORD    = 'fastapi_admin_password'
        DB_NAME        = 'fastapi_admin'
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/PolarisHenry/web-app-teminal.git',
                    branch: 'main'
            }
        }

        stage('Setup Python & Dependencies') {
            steps {
                dir('auto_test') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        playwright install chromium --with-deps
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('auto_test') {
                    sh '''
                        . venv/bin/activate
                        python run_tests.py
                    '''
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                dir('auto_test') {
                    script {
                        allure commandline: 'allure',
                            includeProperties: false,
                            results: [[path: 'reports/allure-results']]
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'auto_test/reports/html/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'auto_test/reports/junit.xml', allowEmptyArchive: true
            junit 'auto_test/reports/junit.xml'
        }
        failure {
            archiveArtifacts artifacts: 'auto_test/reports/allure-results/**/*', allowEmptyArchive: true
        }
    }
}
```

---

## 6. 创建 Jenkins Job

1. Jenkins 首页 → **New Item**
2. 输入名称 `web-app-auto-test`
3. 选择 **Pipeline** → OK
4. Pipeline 配置：
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/PolarisHenry/web-app-teminal.git`
   - Branches to build: `*/main`
   - Script Path: `Jenkinsfile`
5. 保存

---

## 7. 触发构建

### 方式一：手动触发

进入 Job → **Build Now**

### 方式二：定时触发（在 Jenkinsfile 加 triggers）

```groovy
pipeline {
    triggers {
        cron('H 9 * * 1-5')  // 工作日每天早上 9 点
    }
    // ...
}
```

### 方式三：GitHub Webhook（Push 自动触发）

1. Jenkins 安装 **GitHub Integration** 插件
2. Job 配置里勾选 **GitHub hook trigger for GITScm polling**
3. GitHub 仓库 Settings → Webhooks → Add webhook
   - Payload URL: `http://<你的Jenkins地址>:8080/github-webhook/`
   - Content type: `application/json`
   - Events: Just the push event

---

## 8. 查看报告

构建完成后，进入 Job 的某次构建：

- **Allure Report** — 左侧菜单会出现 Allure 报告入口，点击查看美观的测试报告，包括趋势图、用例详情、失败截图等
- **Test Results** — 左侧 Test Results 查看 JUnit 趋势图
- **Artifacts** — 下载归档的 HTML 报告、截图、视频

---

## 9. 目录结构总结

```
web-app-teminal/
├── Jenkinsfile          ← 新增：Jenkins Pipeline 定义
├── auto_test/
│   ├── settings.py      ← 修改：支持环境变量覆盖
│   ├── run_tests.py     ← 测试入口
│   ├── requirements.txt
│   ├── tests/           ← 测试用例
│   └── reports/         ← 测试报告（CI 产出）
└── ...
```

---

## 常见问题

### Q: Jenkins 容器里执行 `playwright install` 报错？

浏览器依赖需要额外的系统库，在 Jenkinsfile 的 Setup 阶段加一步：

```groovy
stage('Setup System Dependencies') {
    steps {
        sh '''
            apt-get update && apt-get install -y \
                libnss3 libnspr4 libatk-bridge2.0-0 libdrm2 \
                libxkbcommon0 libxcomposite1 libxdamage1 \
                libxrandr2 libgbm1 libpango-1.0-0 libcairo2 \
                libasound2 libatspi2.0-0
        '''
    }
}
```

### Q: allure 命令找不到？

确认 Jenkins 全局工具配置里的 Allure 名称和 Jenkinsfile 里 `allure commandline: 'allure'` 一致。

### Q: 后端服务没启动怎么办？

如果有后端代码在仓库里，可以在 Jenkinsfile 加一个 stage 启动：

```groovy
stage('Start Backend') {
    steps {
        sh 'cd backend && docker-compose up -d'
        sh 'sleep 10'  // 等待服务就绪
    }
}
```

如果没有，确保宿主机上的后端服务（3100 端口）在 Jenkins 构建期间处于运行状态。
