pipeline {
    agent any

    parameters {
        choice(
            name: 'TARGET_ENV',
            choices: ['test', 'online'],
            description: '选择测试环境'
        )
    }

    environment {
        // Docker 容器内通过 host.docker.internal 访问宿主机上的被测应用
        BASE_URL       = 'http://host.docker.internal:3100'
        DB_HOST        = 'host.docker.internal'
        DB_PORT        = '3306'
        DB_USER        = 'fastapi_admin'
        DB_PASSWORD    = 'fastapi_admin_password'
        DB_NAME        = 'fastapi_admin'
    }

    stages {
        stage('Run Tests') {
            agent {
                docker {
                    image 'auto-test:latest'
                    reuseNode true
                    args '-u root'
                }
            }
            steps {
                sh '''
                    python run_tests.py
                    chown -R 1000:1000 reports/
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    allure commandline: 'allure',
                        includeProperties: false,
                        results: [[path: 'reports/allure-results']]
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/html/**/*', allowEmptyArchive: true
            archiveArtifacts artifacts: 'reports/junit.xml', allowEmptyArchive: true
            junit testResults: 'reports/junit.xml', allowEmptyResults: true
        }
        failure {
            archiveArtifacts artifacts: 'reports/allure-results/**/*', allowEmptyArchive: true
        }
    }
}
