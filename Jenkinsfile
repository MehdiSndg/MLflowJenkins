pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python:3.11-slim'
        USE_DOCKER = 'false'
    }

    stages {
        stage('Detect environment') {
            steps {
                script {
                    def result = sh(script: 'command -v docker >/dev/null 2>&1', returnStatus: true)
                    env.USE_DOCKER = result == 0 ? 'true' : 'false'
                    if (env.USE_DOCKER == 'true') {
                        echo "Docker detected. Running build in container ${env.DOCKER_IMAGE} as root."
                    } else {
                        echo "Docker not available. Falling back to system Python. Ensure python3 and pip are installed on this agent."
                    }
                }
            }
        }

        stage('Install dependencies') {
            steps {
                script {
                    if (env.USE_DOCKER == 'true') {
                        sh '''
                            docker run --rm -u root -v "$PWD":/workspace -w /workspace ${DOCKER_IMAGE} bash -lc "
                                set -e
                                rm -rf .venv
                                python -m venv .venv
                                . .venv/bin/activate
                                python -m pip install --upgrade pip
                                pip install --no-cache-dir -r requirements.txt
                            "
                        '''
                    } else {
                        sh '''
                            set -e
                            if ! command -v python3 >/dev/null 2>&1; then
                                echo "Python 3 is required when Docker is not available. Install Python 3 + pip on this agent."
                                exit 1
                            fi

                            rm -rf .venv
                            python3 -m venv .venv || {
                                echo "Failed to create virtual environment. Ensure python3-venv (or equivalent) is installed."
                                exit 1
                            }
                            . .venv/bin/activate
                            python -m pip install --upgrade pip
                            pip install --no-cache-dir -r requirements.txt
                        '''
                    fi
                }
            }
        }

        stage('Run training') {
            steps {
                script {
                    if (env.USE_DOCKER == 'true') {
                        sh '''
                            docker run --rm -u root -v "$PWD":/workspace -w /workspace ${DOCKER_IMAGE} bash -lc "
                                set -e
                                . .venv/bin/activate
                                python -m pip install --upgrade pip
                                python train.py
                            "
                        '''
                    } else {
                        sh '''
                            set -e
                            . .venv/bin/activate
                            python train.py
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'mlruns/**,artifacts/**', fingerprint: true
        }
    }
}
