pipeline {
    agent any

    parameters {
     string(name: 'beny14/polybot:${BUILD_NUMBER}', defaultValue: 'INAGE_URL', description: 'deploy polybot')
    }

    stages {
        stage('Deploy') {
            steps {
                sh '''
                    echo "docker push... "
                '''
            }
        }
    }
}
