pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = '0'
        DOCKER_IMAGE = 'streamlit-app'
        REPOSITORY_NAME = 'hayet123/streamlit-app'
    }
    
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Login to Docker') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hayet123', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    sh "docker tag $DOCKER_IMAGE docker.io/$REPOSITORY_NAME:latest"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "docker push docker.io/$REPOSITORY_NAME:latest"
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                echo 'Deploying to server (not implemented in this stage)'
            }
        }
    }
}

