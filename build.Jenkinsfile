pipeline {
    agent any
    stages {
        stage('Build docker image') {
            steps {
            bat '''
              cd polybot
              docker build -t beny14/repo1:polybot-${BUILD_NUMBER} .
              docker login  -u beny14
              docker push beny14/repo1:polybot-${BUILD_NUMBER}
                '''


            }
        }
    }
}