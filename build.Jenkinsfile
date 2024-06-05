pipeline {
    agent any
    stages {
        stage('Build docker image') {
            steps {
                    bat '''
                        cd polybot
                        docker build -t polybot:${BUILD_NUMBER} .
                        docker push beny14/polybot:${BUILD_NUMBER}

                    '''

            }
        }
    }
}