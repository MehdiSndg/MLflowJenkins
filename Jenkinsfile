pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }
    environment {
        C = "1.0"
        MAX_ITER = "200"
    }
    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    set -e
                    apt-get update
                    apt-get install -y python3-venv
                    python --version
                    python -m pip install --upgrade pip
                    pip install --no-cache-dir -r requirements.txt
                '''
            }
        }

        stage('Run training') {
            steps {
                sh 'python train.py'
            }
        }

        stage('Archive results') {
            steps {
                archiveArtifacts artifacts: 'mlruns/**', fingerprint: true
                archiveArtifacts artifacts: 'artifacts/**', fingerprint: true, allowEmptyArchive: true
            }
        }
    }
    post {
        success {
            echo '✅ Build başarıyla tamamlandı. MLflow run oluşturuldu.'
        }
        failure {
            echo '❌ Build başarısız oldu.'
        }
    }
}
