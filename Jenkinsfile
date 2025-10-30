pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh 'python --version'
                sh 'python -m pip install --upgrade pip'
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run training') {
            steps {
                sh 'python train.py'
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'mlruns/**,artifacts/**', fingerprint: true
        }
    }
}
