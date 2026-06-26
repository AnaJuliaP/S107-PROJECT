pipeline {
    agent any
 
    environment {
 
        PYTHON                   = 'python3'
        DOCKER_IMAGE             = 'leticialm/s107-project'
        DOCKER_HUB_CREDENTIAL_ID = 'docker-hub-leticialm'
        EMAIL_REMETENTE            = credentials('EMAIL_REMETENTE')
        EMAIL_DESTINO              = credentials('EMAIL_DESTINO')
    }
 
    stages {
   
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
 
        stage('Docker Build e Push') {
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
                            -f Dockerfile.jenkins \\
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
 
        stage('Notificação')
        {
            steps
            {
                withEnv([
                    "STATUS_BUILD=${currentBuild.currentResult}",
                ]) {
                    sh 'python3 scripts/notificar.py'
                }
            }
        }
    }
 
    post
    {
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