pipeline {
    agent any
    environment {
        DOCKER_BUILDKIT = '1'  // Active le mode BuildKit pour Docker (optionnel)
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
                    sh 'ls -la'
                    sh 'docker build -t streamlit-app .'
                }
            }
        }
        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8501:8501 streamlit-app'
            }
        }
    }
}
