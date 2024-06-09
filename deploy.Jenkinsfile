pipeline {
    agent any

    parameters {
     string(name: 'beny14/polybot:${BUILD_NUMBER}', defaultValue: 'INAGE_URL', description: 'deploy polybot')
    }

    stages {
        stage('Deploy') {
            steps {
                bat '''
                    echo "deploying to k8s cluster ..( or any other alternative)"
                '''
            }
        }
    }
}