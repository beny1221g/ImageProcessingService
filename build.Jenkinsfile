pipeline {
    options {
        buildDiscarder(logRotator(daysToKeepStr: '14'))
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
                        pylint --disable=C0301 polybot/*.py
                        pylint --disable=C0114 polybot/*.py
                        pylint --disable=E1101 polybot/*.py
                        pylint --disable=C0116 polybot/*.py
                        pylint --disable=C0103 polybot/*.py
                        pylint --disable=W0718 polybot/*.py
                        pylint --disable=E0401 polybot/*.py
                        pylint --disable=W0613 polybot/*.py
                        python3 -m pylint polybot/*.py
                        deactivate
                        '''
                    }
                }
            }
        }
    } // End of stages block

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