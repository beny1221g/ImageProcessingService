pipeline {
    // Add pipeline options
    options {
        buildDiscarder(logRotator(daysToKeepStr: '30'))
        disableConcurrentBuilds()
        timestamps()
    }

    // Define environment variables
    environment {
        IMG_NAME = "polybot:${BUILD_NUMBER}"
    }

    agent {
        docker {
            image 'beny14/dockerfile_agent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Build') {
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

        stage('Test') {
            steps {
                script {
                    // Run pylint with PYTHONPATH set
                    sh '''
                    python3 -m plint *.py
                    '''

                }
            }
        }
    }

    post {
        always {
            // Clean up old containers but not the new one
            script {
                // Fetch the container ID of the currently running container
                def containerId = sh(script: "docker ps -q -f ancestor=${IMG_NAME}", returnStdout: true).trim()

                // Remove all stopped containers with the same image except the current one
                sh """
                    for id in \$(docker ps -a -q -f ancestor=${IMG_NAME}); do
                        if [ "\$id" != "${containerId}" ]; then
                            docker rm -f \$id || true
                        fi
                    done
                """
            }

            // Clean up built Docker images from disk
            script {
                sh 'docker rmi $IMG_NAME || true'
            }

            // Clean build artifacts from Jenkins server
            cleanWs()
        }
    }
}