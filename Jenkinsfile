pipeline {
    agent any

    environment {
        IMAGE_NAME = "wha02068/django-test"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/KIMHAUN/django-test.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:${BUILD_NUMBER} .'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_NAME:${BUILD_NUMBER}'
            }
        }

        stage('Update Deployment YAML') {
            steps {
                sh '''
                cd k8s
                sed -i "s|image:.*|image: $IMAGE_NAME:${BUILD_NUMBER}|" deployment.yaml
                git add deployment.yaml
                git commit -m "Update image to ${BUILD_NUMBER}"
                git push
                '''
            }
        }
    }
}
