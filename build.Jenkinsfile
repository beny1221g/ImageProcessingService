pipeline {
    options {
        buildDiscarder(logRotator(daysToKeepStr: '14'))
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMG_NAME = "polybot:${BUILD_NUMBER}"
        DOCKER_REPO = "beny14/polybot"
        SNYK_TOKEN = credentials('SNYK_TOKEN')
    }

    agent {
        docker {
            image 'beny14/dockerfile_agent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
            TELEGRAM_TOKEN = credentials('TELEGRAM_TOKEN')
        }
    }

    stages {
        stage('Build') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_key', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        try {
                            sh """
                                echo ${USERPASS} | docker login -u ${USERNAME} --password-stdin
                                docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
                                docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${DOCKER_REPO}:latest
                                docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                            """
                        } catch (Exception e) {
                            error "Build failed: ${e.getMessage()}"
                        }
                    }
                }
            }
        }

        stage('Snyk Scan') {
            steps {
                withCredentials([string(credentialsId: 'SNYK_TOKEN', variable: 'SNYK_TOKEN')]) {
                    script {
                        try {
                            sh """
                                snyk auth ${SNYK_TOKEN}
                                snyk config set disableSuggestions=true
                                snyk container test ${DOCKER_REPO}:${BUILD_NUMBER} || echo "Snyk scan failed"
                            """
                        } catch (Exception e) {
                            error "Snyk scan failed: ${e.getMessage()}"
                        }
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
                        pip install -r requirements.txt
                        python3 -m pytest --junitxml results.xml polybot/*.py
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
                            // Record issues using a general method if available, or simply echo the log
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