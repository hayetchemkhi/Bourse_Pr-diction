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

        // Désactiver BuildKit après le checkout
        stage('Disable BuildKit') {
            steps {
                script {
                    // Désactive BuildKit si nécessaire
                    env.DOCKER_BUILDKIT = '0'
                }
            }
        }

        // Construction de l'image Docker
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t ${IMAGE_NAME} .'
                }
            }
        }

        // Push de l'image Docker vers Docker Hub
        stage('Push Docker Image') {
            steps {
                script {
                    // Connexion à Docker Hub avec les informations d'identification de Jenkins
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin'
                        sh 'docker tag ${IMAGE_NAME} ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest'
                        sh 'docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest'
                    }
                }
            }
        }

        // Déploiement de l'image Docker sur un serveur distant
        stage('Deploy to Server') {
            steps {
                script {
                    sh 'ssh hayet@10.0.2.15 "docker pull ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest"'
                }
            }
        }
    }
}

