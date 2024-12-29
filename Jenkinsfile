pipeline {
    agent any
    environment {
        DOCKER_BUILDKIT = '1'
        IMAGE_NAME = 'streamlit-app'
        DOCKER_REGISTRY = 'docker.io'
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/hayetchemkhi/Bourse_Pr-diction.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t ${IMAGE_NAME} .'
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Login to Docker Hub using Jenkins credentials
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                        sh 'docker tag ${IMAGE_NAME} ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest'
                        sh 'docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest'
                    }
                }
            }
        }
        stage('Deploy to Server') {
            steps {
                script {
                    sh 'ssh user@server "docker pull ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest && docker run -d -p 8501:8501 ${DOCKER_REGISTRY}/${IMAGE_NAME}"'
                }
            }
        }
    }
}
