pipeline {
  agent any
  tools {git 'Default'}

  environment {
    DEPLOY_USER = 'admin
    '
    DEPLOY_HOST = 'localhost:8070'
    DEPLOY_DIR  = '/home/mysite/mysite'
    REPO_URL    = 'https://github.com/KIMHAUN/django-test.git'
    BRANCH      = 'main'
    SSH_CRED_ID = 'deploy-ssh-key'   // Jenkins에 만든 credentials ID
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Run Remote Deploy') {
      steps {
        sshagent (credentials: [env.SSH_CRED_ID]) {
          // 배포 스크립트가 레포에 있으므로 원격에서 바로 실행
          bat """
            ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'bash -s' <<'ENDSSH'
              set -e
              # ensure git is available on remote and script dir exists
              mkdir -p ${DEPLOY_DIR}
              cd ${DEPLOY_DIR}
              # pull or clone handled by deploy_remote.sh
              curl -s -o /tmp/deploy_remote.sh https://raw.githubusercontent.com/KIMHAUN/django-test/${BRANCH}/scripts/deploy_remote.sh
              chmod +x /tmp/deploy_remote.sh
              /tmp/deploy_remote.sh
            ENDSSH
          """
        }
      }
    }
  }

  post {
    success { echo "Deployment succeeded" }
    failure { echo "Deployment failed" }
  }
}



