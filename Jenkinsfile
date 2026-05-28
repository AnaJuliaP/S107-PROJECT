pipeline {
    agent any

    environment {

        PYTHON                   = 'python3'
        DOCKER_IMAGE             = 'leticialm/s107-project'
        DOCKER_HUB_CREDENTIAL_ID = 'docker-hub-leticialm'
        EMAIL_REMETENTE            = credential('EMAIL_REMETENTE')
        EMAIL_DESTINO              = credential('EMAIL_DESTINO')
        STATUS_BUILD               = ${currentBuild.currentResult}
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Instalar Dependências do Projeto') {
            steps {
                sh '''
                    python3 -m pip install --break-system-packages --user \
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
                    python3 -m pytest tests/ \
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
                                     fingerprint: true,
                                     allowEmptyArchive: true
                }
            }
        }

        stage('Build') {
            steps {
                sh 'python3 -m build'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/**',
                                     fingerprint: true
                }
            }
        }

        stage('Notificação') 
        {
            steps 
            {
                    sh 'python3 scripts/notificar.py'
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
