pipeline {
    agent any
    stages {
        stage('Build docker image') {
            steps {
                    sh '''
                        cd polybot
                        docker build -t polybot:${BUILD_NUMBER} .
                        docker push docker push beny14/polybot:${BUILD_NUMBER}

                    '''

            }
        }
    }
}