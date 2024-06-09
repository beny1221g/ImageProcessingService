pipeline {
    agent any

    parameters {
     string(name: 'beny14/polybot', defaultValue: 'INAGE_URL', description: 'deploy polybot')
    }

    stages {
        stage('Deploy') {
            steps {
                sh '''
                    echo "deploying to k8s cluster ..( or any other alternative)"
                '''
            }
        }
    }
}