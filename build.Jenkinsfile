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
                        bat """
                            @echo off
                            cd polybot
                            echo Logging  in to Docker...
                            echo %USERPASS% | docker login -u %USERNAME% --password-stdin
                            if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                            echo Building Docker image...
                            docker build -t %IMG_NAME% .
                            if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                            echo Tagging Docker image...
                            docker tag %IMG_NAME% beny14/%IMG_NAME%
                            if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                            echo Pushing Docker image...
                            docker push beny14/%IMG_NAME%
                            if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        """
                    }
                }
            }
        }
    }
}