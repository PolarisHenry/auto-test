pipeline {
    // agent any: 在任意可用 Jenkins agent 上运行（实际执行测试的是下方 Docker agent）
    agent any

    // ==================== 构建参数 ====================
    // 构建时可从下拉框选择目标环境，值会作为环境变量 TARGET_ENV 传入
    // settings.py 读取后定位到 ENV.test / ENV.online 对应的地址
    parameters {
        choice(
            name: 'TARGET_ENV',
            choices: ['test', 'online'],
            description: '选择测试环境'
        )
    }

    // ==================== 环境变量 ====================
    // 被测应用的访问地址和数据库连接信息，测试代码通过 os.environ 自动读取
    //
    // 不同部署场景下 BASE_URL 的配置：
    //   本地 Docker Desktop：  http://host.docker.internal:3100  （容器→宿主机，仅 Mac/Windows 有效）
    //   内网测试服务器：        http://test.yourcompany.com         （标准域名，不暴露端口）
    //   K8s 集群：             http://app-svc.namespace             （集群内 Service DNS）
    //
    // 只需改这里，settings.py 中 env.base_url 自动返回对应地址，测试代码无需修改。
    environment {
        BASE_URL       = 'http://host.docker.internal:3100'
        DB_HOST        = 'host.docker.internal'
        DB_PORT        = '3306'
        DB_USER        = 'fastapi_admin'
        DB_PASSWORD    = 'fastapi_admin_password'
        DB_NAME        = 'fastapi_admin'
    }

    stages {
        // ==================== 阶段①：运行测试 ====================
        stage('Run Tests') {
            agent {
                docker {
                    image 'auto-test:latest'
                    // reuseNode true: 复用顶层 agent 的 workspace（git 检出的代码目录）
                    //    通过 volumes-from 挂载到容器内，所以代码变更无需重新 build 镜像
                    reuseNode true
                    // -u root: 以 root 运行，避免容器内文件权限问题
                    // Jenkins 的 environment 变量（TARGET_ENV、BASE_URL 等）自动传入容器
                    args '-u root'
                }
            }
            steps {
                sh '''
                    python run_tests.py
                    chown -R 1000:1000 reports/          # 将产物改为宿主机用户所有，确保后续阶段可读
                '''
            }
        }

        // ==================== 阶段②：生成 Allure 报告 ====================
        // 使用 Jenkins 宿主机安装的 Allure CLI 生成 HTML 报告
        // 容器内不安装 allure（减少镜像体积），测试阶段只产出 allure-results 原始数据
        stage('Generate Allure Report') {
            steps {
                script {
                    allure commandline: 'allure',
                        includeProperties: false,        // 不在报告中展示环境变量，避免泄露密码
                        results: [[path: 'reports/allure-results']]
                }
            }
        }
    }

    // ==================== 后置操作 ====================
    post {
        // always: 无论构建成功还是失败都执行
        always {
            // 归档 Allure HTML 报告，Jenkins 页面上可浏览器查看
            archiveArtifacts artifacts: 'reports/html/**/*', allowEmptyArchive: true
            // 归档 JUnit XML，供 Jenkins 趋势图和通过率统计使用
            archiveArtifacts artifacts: 'reports/junit.xml', allowEmptyArchive: true
            // 发布 JUnit 测试结果，Jenkins 首页展示通过/失败趋势
            junit testResults: 'reports/junit.xml', allowEmptyResults: true
        }
        // failure: 仅构建失败时执行
        failure {
            // 归档 Allure 原始结果（含截图、视频），便于排查失败原因
            archiveArtifacts artifacts: 'reports/allure-results/**/*', allowEmptyArchive: true
        }
        // 注：success 和 unstable 未做特殊处理
        //   success  → 产物已在 always 中归档
        //   unstable → 测试结果已通过 junit 发布，Jenkins 自动标记
    }
}
