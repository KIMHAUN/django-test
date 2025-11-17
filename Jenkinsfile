pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/KIMHAUN/django-test.git'
      }
    }

    stage('Build Docker') {
      steps {
        sh 'docker build -t wha02068/django:${BUILD_NUMBER} .'
      }
    }

    stage('Push Docker') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'echo $PASS | docker login -u $USER --password-stdin'
          sh 'docker push wha02068/django:${BUILD_NUMBER}'
        }
      }
    }

    stage('Update k8s yaml') {
      steps {
        sh '''
          sed -i "s|image: .*|image: wha02068/django:${BUILD_NUMBER}|g" k8s/deployment.yaml
        '''
      }
    }

    stage('Push GitHub') {
      steps {
        sh '''
          git config user.email "jenkins@ci"
          git config user.name "Jenkins CI"
          git commit -am "Deploy build ${BUILD_NUMBER}"
          git push origin main
        '''
      }
    }
  }
}
