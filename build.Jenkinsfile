pipeline {
    options {
        buildDiscarder(logRotator(daysToKeepStr: '14'))
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMG_NAME = "polybot:${BUILD_NUMBER}"
        DOCKER_REPO = "http://192.168.1.75:8081/#browse/browse:docker-hosted" // Update with your Nexus Docker repository URL
        NEXUS_USER = credentials('nexus_user')
        NEXUS_PASS = credentials('nexus_pass')
        SNYK_TOKEN = credentials('SNYK_TOKEN')
        TELEGRAM_TOKEN = credentials('TELEGRAM_TOKEN')
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
                script {
                    try {
                        echo "Logging into Nexus Docker repository with user: ${NEXUS_USER_USR}"
                        sh """
                            echo ${NEXUS_USER_PSW} | docker login -u ${NEXUS_USER_USR} --password-stdin ${DOCKER_REPO}
                            docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
                            docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${DOCKER_REPO}:latest
                            docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                            docker push ${DOCKER_REPO}:latest
                        """
                    } catch (Exception e) {
                        error "Build failed: ${e.getMessage()}"
                    }
                }
            }
        }

        stage('Unit Test') {
            steps {
                script {
                    docker.image("${DOCKER_REPO}:${BUILD_NUMBER}").inside {
                        sh """
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install pytest-xdist
                        python3 -m pytest -n auto --junitxml results.xml polybot/*.py
                        deactivate
                        """
                    }
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'results.xml'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        docker.image("${DOCKER_REPO}:${BUILD_NUMBER}").inside {
                            sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install -r requirements.txt
                            pylint --disable=E1136,C0301,C0114,E1101,C0116,C0103,W0718,E0401,W0613,R1722,W0612,R0912,C0304,C0115,R1705 polybot/*.py > pylint.log || true
                            ls -alh
                            cat pylint.log
                            deactivate
                            '''
                        }
                    } catch (Exception e) {
                        error "Test failed: ${e.getMessage()}"
                    }
                }
            }
            post {
                always {
                    script {
                        try {
                            archiveArtifacts artifacts: 'pylint.log', allowEmptyArchive: true
                            echo "Pylint log content:"
                            sh 'cat pylint.log'
                        } catch (Exception e) {
                            echo "Archiving or recording issues failed: ${e.getMessage()}"
                        }
                    }
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

        failure {
            script {
                def errorMessage = currentBuild.result == 'FAILURE' ? currentBuild.description : 'Build failed'
                echo "Error occurred: ${errorMessage}"
            }
        }
    }
}
