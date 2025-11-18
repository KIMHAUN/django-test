pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKERHUB_REPO = "wha02068/django-test"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Git Repo 최신 내용 가져오기"
                checkout scm

            }
        }

        stage('Set Version') {
            steps {
                script {
                    env.VERSION = "v${BUILD_NUMBER}"
                    env.IMAGE_TAG = "${DOCKERHUB_REPO}:${env.VERSION}"

                    echo "Build Version: ${env.VERSION}"
                    echo "Docker Image Tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh """
                docker build -t ${IMAGE_TAG} .
                """
            }
        }

        stage('Docker Login') {
            steps {
                sh """
                echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                """
            }
        }

        stage('Docker Push') {
            steps {
                sh """
                docker push ${IMAGE_TAG}
                """
            }
        }

        stage('Update Deployment YAML') {
            steps {
                sh """
                sed -i "s|image:.*|image: ${IMAGE_TAG}|" k8s/deployment.yaml
                git config user.email "jenkins@pipeline"
                git config user.name "jenkins"

                git pull origin main --rebase
                
                git add k8s/deployment.yaml
                git commit -m "Update image to ${env.VERSION}"
                git push origin main
                """
            }
        }
    }

    post {
        success {
            echo "성공적으로 Docker Hub push 및 ArgoCD 배포 업데이트 완료!"
        }
        failure {
            echo "빌드 실패! 콘솔 로그를 확인하세요."
        }
    }
}
