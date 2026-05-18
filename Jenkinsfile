pipeline {
    agent any

    environment {
        DOCKER_USER = "syugesh"
        DOCKER_CREDS = "dockerhub-creds"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'
            }
        }

        stage('Build Images') {
            steps {
                sh 'docker build -t $DOCKER_USER/survey-backend:latest ./backend'
                sh 'docker build -t $DOCKER_USER/survey-frontend:latest ./frontend'
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "$DOCKER_CREDS",
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )]) {
                    sh 'echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin'
                    sh 'docker push $DOCKER_USER/survey-backend:latest'
                    sh 'docker push $DOCKER_USER/survey-frontend:latest'
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                sh '''
                docker pull $DOCKER_USER/survey-backend:latest
                docker pull $DOCKER_USER/survey-frontend:latest
                docker compose down || true
                docker compose up -d
                docker ps
                '''
            }
        }
    }
}
