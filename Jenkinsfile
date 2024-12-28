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
                sh 'docker build -t streamlit-app .'
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Utiliser les credentials Docker
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin'
                        sh 'docker tag streamlit-app docker.io/hayetchemkhi/streamlit-app:latest'
                        sh 'docker push docker.io/hayetchemkhi/streamlit-app:latest'
                    }
                }
            }
        }
        stage('Deploy to Server') {
            steps {
                script {
                    sh 'ssh user@server "docker pull docker.io/hayetchemkhi/streamlit-app:latest"'
                    sh 'ssh user@server "docker run -d -p 8501:8501 hayetchemkhi/streamlit-app:latest"'
                }
            }
        }
    }
}

