pipeline {
    agent any

    environment {
        DOCKER_USER = "syugesh"
        DOCKER_CREDS = "dockerhub-creds"
    }

    stages {

        stage('Build Images') {
            steps {
                sh 'docker build -t $DOCKER_USER/survey-backend:latest ./backend'
                sh 'docker build -t $DOCKER_USER/survey-frontend:latest ./frontend'
            }
        }

        stage('Push Images') {
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

        stage('Deploy') {
            steps {
                sh '''
		docker compose pull
                docker compose down || true
                docker compose up -d
                '''
            }
        }
    }
}
 
