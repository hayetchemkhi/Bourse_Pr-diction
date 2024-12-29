pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'votre-utilisateur/streamlit-app:latest'
    }
    stages {
        stage('Cloner le Code') {
            steps {
                git url: 'https://github.com/[votre-username]/streamlit-app.git'
            }
        }
        stage('Installer les Dépendances') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Exécuter les Tests Unitaires') {
            steps {
                sh 'pytest test_app.py'
            }
        }
        stage('Construire l\'Image Docker') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }
        stage('Pousser vers Docker Hub') {
            steps {
                sh 'docker push $DOCKER_IMAGE'
            }
        }
        stage('Déployer sur Fly.io') {
            steps {
                sh 'flyctl deploy'
            }
        }
    }
}
