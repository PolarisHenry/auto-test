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
        stage('Run Tests') {
            agent {
                docker {
                    image 'auto-test:latest'
                    reuseNode true
                    args '-u root'
                }
            }
            steps {
                dir('auto_test') {
                    sh '''
                        python run_tests.py
                        chown -R 1000:1000 reports/
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
            junit testResults: 'auto_test/reports/junit.xml', allowEmptyResults: true
        }
        failure {
            archiveArtifacts artifacts: 'auto_test/reports/allure-results/**/*', allowEmptyArchive: true
        }
    }
}
