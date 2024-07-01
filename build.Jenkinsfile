pipeline {
    options {
        buildDiscarder(logRotator(daysToKeepStr: '3'))
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
                        sh """
                            echo ${USERPASS} | docker login -u ${USERNAME} --password-stdin
                            docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
                            docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${DOCKER_REPO}:latest
                            docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                        """
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image("${DOCKER_REPO}:${BUILD_NUMBER}").inside {
                        sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        python3 -m pylint polybot/*.py
                        deactivate
                        '''
                    }
                }
            }
        }


    post {
        always {
            script {
                def containerId = sh(script: "docker ps -q -f ancestor=${DOCKER_REPO}:${BUILD_NUMBER}", returnStdout: true).trim()

                sh """
                    for id in \$(docker ps -a -q -f ancestor=${DOCKER_REPO}:${BUILD_NUMBER}); do
                        if [ "\$id" != "${containerId}" ]; then
                            docker rm -f \$id || true
                        fi
                    done
                """
            }
            script {
                sh """
                    docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | grep '${DOCKER_REPO}' | grep -v ':latest' | grep -v ':${BUILD_NUMBER}' | awk '{print \$2}' | xargs --no-run-if-empty docker rmi -f || true
                """
            }

            cleanWs()
        }
    }

}