pipeline {
    agent any
    stages {
        stage('Build docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_key', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        bat """
                            @echo off
                            cd polybot
                            echo %USERPASS% | docker login -u %USERNAME% --password-stdin
                            docker build -t beny14/repo1:%BUILD_NUMBER% .
                            docker push beny14/repo1:%BUILD_NUMBER%
                        """
                    }
                }
            }
        }
    }
}