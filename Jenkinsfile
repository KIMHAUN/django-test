pipeline {
  agent any
  tools {git 'Default'}

  environment {
    DEPLOY_USER = 'DS 13'
    DEPLOY_HOST = 'localhost'
    DEPLOY_DIR  = 'D:\\deploy\\djang-otest'
    REPO_URL    = 'https://github.com/KIMHAUN/django-test.git'
    BRANCH      = 'main'
    SSH_CRED_ID = 'deploy-ssh-key'   // Jenkins에 만든 credentials ID
  }

  stages {
    stage('Deploy') {
      steps {
        bat """
          ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no "%SSH_USER%"@localhost "echo Connected && whoami"
        """
      }
    }
  }

  post {
    success { echo "Deployment succeeded" }
    failure { echo "Deployment failed" }
  }
}



