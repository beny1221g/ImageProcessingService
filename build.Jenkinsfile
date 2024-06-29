pipeline {
    options {
        buildDiscarder(logRotator(daysToKeepStr: '30'))
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMG_NAME = "polybot:${BUILD_NUMBER}"
        DOCKER_REPO = "beny14/polybot"
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
                            docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
                            docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${DOCKER_REPO}:latest
                            docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                            docker push ${DOCKER_REPO}:latest
                        """
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run pylint in a virtual environment
                    sh '''
                    cd polybot
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python3 -m pylint *.py
                    deactivate
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
                def containerId = sh(script: "docker ps -q -f ancestor=${DOCKER_REPO}:${BUILD_NUMBER}", returnStdout: true).trim()

                // Remove all stopped containers with the same image except the current one
                sh """
                    for id in \$(docker ps -a -q -f ancestor=${DOCKER_REPO}:${BUILD_NUMBER}); do
                        if [ "\$id" != "${containerId}" ]; then
                            docker rm -f \$id || true
                        fi
                    done
                """
            }

            // Clean up old Docker images but keep the new one
            script {
                sh """
                    docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | grep '${DOCKER_REPO}' | grep -v ':latest' | grep -v ':${BUILD_NUMBER}' | awk '{print \$2}' | xargs --no-run-if-empty docker rmi -f || true
                """
            }

            // Clean build artifacts from Jenkins server
            cleanWs()
        }
    }
}
