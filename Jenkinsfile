pipeline {
    agent any

    environment {
        PYTHON                   = 'python3'
        PIP                      = 'pip3'
        DOCKER_IMAGE             = 'leticialm/s107-project'
        DOCKER_HUB_CREDENTIAL_ID = 'docker-hub-leticialm'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Instalar Dependências') {
            steps {
                sh '''
                    apt-get update -qq
                    apt-get install -y python3 python3-pip python3-venv docker.io
                    pip3 install --break-system-packages \
                        pytest \
                        pytest-cov \
                        pytest-html \
                        build \
                        -r requirements.txt
                '''
            }
        }

        stage('Testes') {
            steps {
                sh '''
                    ${PYTHON} -m pytest tests/ \
                        --cov=src \
                        --cov-report=term-missing \
                        --cov-report=xml:coverage.xml \
                        --html=report.html \
                        --self-contained-html \
                        -v
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'report.html, coverage.xml',
                                     fingerprint: true
                }
            }
        }

        stage('Build') {
            steps {
                sh '${PYTHON} -m build'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/**',
                                     fingerprint: true
                }
            }
        }

        stage('Docker Build e Push (Docker Hub)') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: env.DOCKER_HUB_CREDENTIAL_ID,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh """
                        set -e
                        echo \$DOCKER_TOKEN | docker login -u \$DOCKER_USER --password-stdin
                        docker build \\
                            -t ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER} \\
                            -t ${env.DOCKER_IMAGE}:latest \\
                            .
                        docker push ${env.DOCKER_IMAGE}:${env.BUILD_NUMBER}
                        docker push ${env.DOCKER_IMAGE}:latest
                        docker logout || true
                    """
                }
            }
        }

        stage('Notificação') {
            steps {
                script {
                    def buildStatus = currentBuild.currentResult
                    def jobName     = env.JOB_NAME
                    def buildNumber = env.BUILD_NUMBER
                    def buildUrl    = env.BUILD_URL

                    sh """
                        ${PYTHON} scripts/notificar.py \
                            --status  '${buildStatus}' \
                            --job     '${jobName}' \
                            --build   '${buildNumber}' \
                            --url     '${buildUrl}'
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline encerrado | Status: ${currentBuild.currentResult}"
        }
        success {
            echo "Todos os testes passaram e o pacote foi gerado com sucesso."
        }
        failure {
            echo "Pipeline falhou. Verifique os logs, o report.html e o coverage.xml."
        }
    }
}