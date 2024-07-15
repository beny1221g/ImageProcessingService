pipeline {
    options {
        buildDiscarder(logRotator(daysToKeepStr: '14'))
        disableConcurrentBuilds()
        timestamps()
        timeout(time: 120, unit: 'MINUTES') // Set a global timeout for the pipeline
    }

    environment {
        IMG_NAME = "polybot:${BUILD_NUMBER}"
        DOCKER_REPO = "beny14/polybot"
        SNYK_TOKEN = credentials('SNYK_TOKEN')
        TELEGRAM_TOKEN = credentials('TELEGRAM_TOKEN')
        NEXUS_CREDENTIAL = credentials('nexus_user') // Replace with your Nexus credentials ID
        NEXUS_REPO_URL = "http://192.168.1.75:5000/repository/docker-repo/" // Replace with your Nexus repository  URL
    }

    agent {
        docker {
            image 'beny14/dockerfile_agent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Check and Start Nexus') {
            steps {
                script {
                    def nexusStatus = sh(script: 'docker ps -q -f name=nexus', returnStdout: true).trim()
                    if (nexusStatus == "") {
                        echo "Nexus container is not running, checking if it exists..."
                        def nexusExists = sh(script: 'docker ps -a -q -f name=nexus', returnStdout: true).trim()
                        if (nexusExists != "") {
                            echo "Stopping and removing existing Nexus container"
                            sh 'docker stop nexus && docker rm nexus'
                        }
                        echo "Starting Nexus container"
                        sh 'docker run -d -p 8081:8081 --name nexus -v /path/to/nexus-data:/nexus-data sonatype/nexus3'
                    } else {
                        echo "Nexus container is already running"
                    }
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "nexus_user", usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                        try {
                            echo "Starting Docker build"
                            sh """
                                echo ${NEXUS_PASS} | docker login -u ${NEXUS_USER} --password-stdin ${NEXUS_REPO_URL}
                                docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
                                docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${DOCKER_REPO}:latest
                                docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${NEXUS_REPO_URL}${DOCKER_REPO}:${BUILD_NUMBER}
                                docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${NEXUS_REPO_URL}${DOCKER_REPO}:latest
                                docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                                docker push ${DOCKER_REPO}:latest
                                docker push ${NEXUS_REPO_URL}${DOCKER_REPO}:${BUILD_NUMBER}
                                docker push ${NEXUS_REPO_URL}${DOCKER_REPO}:latest
                            """
                            echo "Docker build and push completed"
                        } catch (Exception e) {
                            error "Build failed: ${e.getMessage()}"
                        }
                    }
                }
            }
        }

        stage('Unit Test') {
            steps {
                script {
                    echo "Starting Unit Tests"
                    docker.image("${DOCKER_REPO}:${BUILD_NUMBER}").inside {
                        sh """
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        pip install pytest-xdist pytest-timeout
                        # Run pytest with verbosity and timeout for each test
                        python3 -m pytest -n 4 --timeout=60 --junitxml results.xml tests/*.py
                        deactivate
                        """
                    }
                    echo "Unit Tests completed"
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
                        echo "Starting Lint Tests"
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
                        echo "Lint Tests completed"
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
                echo "Cleaning up Docker containers and images"
                def containerId = sh(script: "docker ps -q -f ancestor=${DOCKER_REPO}:${BUILD_NUMBER}", returnStdout: true).trim()

                sh """
                    for id in \$(docker ps -a -q -f ancestor=${DOCKER_REPO}:${BUILD_NUMBER}); do
                        if [ "\$id" != "${containerId}" ]; then
                            docker rm -f \$id || true
                        fi
                    done
                """
                sh """
                    docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | grep '${DOCKER_REPO}' | grep -v ':latest' | grep -v ':${BUILD_NUMBER}' | awk '{print \$2}' | xargs --no-run-if-empty docker rmi -f || true
                """
                cleanWs()
                echo "Cleanup completed"
            }
        }

        failure {
            script {
                def errorMessage = currentBuild.result == 'FAILURE' ? currentBuild.description : 'Build failed'
                echo "Error occurred: ${errorMessage}"
            }
        }
    }
}
