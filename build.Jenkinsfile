pipeline {
    agent any

enviroment{
     IMG_NAME = "polybot:${BUILD_NUMBER}"

    stages {
        stage('Build docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_key', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                     {
                        bat """
                            @echo off
                            cd polybot
                            docker login -u %USERNAME% -p $USERPASS% --password-stdin
                            docker build -t %IMG_NAME% .
                            docker tag %IMG_NAME% beny14/%IMG_NAME%
                            docker push beny14/%IMG_NAME%
                        """

                }
            }
        }
    }
}
}