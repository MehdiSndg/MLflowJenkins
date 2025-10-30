pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python:3.11-slim'
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    docker run --rm -u root -v "$PWD":/workspace -w /workspace ${DOCKER_IMAGE} bash -lc "
                        set -e
                        python --version
                        python -m pip install --upgrade pip
                        pip install --no-cache-dir -r requirements.txt
                    "
                '''
            }
        }

        stage('Run training') {
            steps {
                sh '''
                    docker run --rm -u root -v "$PWD":/workspace -w /workspace ${DOCKER_IMAGE} bash -lc "
                        set -e
                        pip install --no-cache-dir -r requirements.txt
                        python train.py
                    "
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'mlruns/**,artifacts/**', fingerprint: true
        }
    }
}
