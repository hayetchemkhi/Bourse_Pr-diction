pipeline {
    agent any

    environment {
        IMAGE_NAME = 'streamlit-app'
        DOCKER_REGISTRY = 'docker.io' // ou ton propre registre
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
                    // Construire l'image Docker
                    sh 'docker build -t ${IMAGE_NAME} .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Push de l'image Docker vers un registre
                    sh 'docker push ${IMAGE_NAME}'
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                script {
                    // Déploiement de l'application, selon ton serveur cible
                    sh 'ssh user@server "docker pull ${IMAGE_NAME} && docker run -d -p 8501:8501 ${IMAGE_NAME}"'
                }
            }
        }
    }
}
