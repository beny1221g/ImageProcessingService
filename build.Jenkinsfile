pipeline {
    agent any

    environment {
        IMG_NAME = "polybot:${BUILD_NUMBER}"
    }

    stages {
        stage('Build docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_key', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        // Use correct Docker login syntax
                        bat """
                            @echo off
                            cd polybot
                            docker login -u %USERNAME% -p %USERPASS%
                            docker build -t %IMG_NAME% .
                            docker tag %IMG_NAME% beny14/repo1:%IMG_NAME%
                            docker push beny14/repo1:%IMG_NAME%
                        """
                    }
                }
            }
        }
//         stage('Trigger Deploy'){
//         steps job: 'ploybotdeploy',wait:false, parameters:[
//         string(name:'beny14/repo1:%IMG_NAME%', value:"beny14/repo1:%IMG_NAME%")]}
    }
}
