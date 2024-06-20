pipeline {

    agent {
        dockerContainer {
            image 'beny14/dockerfile_agent:latest'
            label 'my-docker-agent'
            args '-v /var/lib/jenkins/workspace:/workspace'
        }
    }

    environment {
        IMG_NAME = "polybot:${BUILD_NUMBER}"
    }

    stages {
        stage('Build docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_key', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        // Use correct Docker login syntax
                        sh """
                            cd polybot
                            echo ${USERPASS} | docker login -u ${USERNAME} --password-stdin
                            docker build -t ${IMG_NAME} .
                            docker tag ${IMG_NAME} beny14/${IMG_NAME}
                            docker push beny14/${IMG_NAME}
                        """
                    }
                }
            }
        }
        stage('Trigger Deploy') {
            steps {
                build job: 'deploy_polybot', wait: false, parameters: [
                    string(name: 'beny14/$IMG_NAME', value: IMG_NAME)
                ]
            }
        }
    }
}
