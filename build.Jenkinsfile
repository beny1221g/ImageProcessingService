pipeline {
    agent any
    stages {
        stage('Build docker image') {
            steps {
            withCredentials(
                 [usernamePassword(credentialsId: 'dockerhub_key', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]
              ) {
            bat '''
              cd polybot
              docker login -u $USERNAME -p $USERPASS
              docker build -t polybot:${BUILD_NUMBER} .

              docker push beny14/repo1:polybot-${BUILD_NUMBER}
                '''


            }
            }
        }
    }
}