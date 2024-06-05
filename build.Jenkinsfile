pipeline {
    agent any
    stages {
        stage('Build docker image') {
            steps {
                    bat '''
                        cd polybot
                        docker build -t polybot:${BUILD_NUMBER} .
                        REM Change directory to where Docker executable is located
                        cd "C:\Program Files\Docker"

                        REM Run Docker with elevated privileges
                        docker.exe %*



                        docker push beny14/repo1:polybot

                    '''

            }
        }
    }
}