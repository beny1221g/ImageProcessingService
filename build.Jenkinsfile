@Library('shared-lib') _ // Import the shared library named 'shared-lib' to use its functions

pipeline {
    options {
        buildDiscarder(logRotator(daysToKeepStr: '14')) // Retain build logs for 14 days before discarding them
        disableConcurrentBuilds() // Prevent multiple instances of this pipeline from running simultaneously
        timestamps() // Add timestamps to the build logs for tracking
        timeout(time: 40, unit: 'MINUTES') // Set a global timeout of 40 minutes for the entire pipeline
    }

    environment {
        IMG_NAME = "polybot:${BUILD_NUMBER}" // Define the Docker image name with the build number
        DOCKER_REPO = "beny14/polybot" // Define the Docker repository name
        SNYK_TOKEN = credentials('SNYK_TOKEN') // Retrieve Snyk token from Jenkins credentials store
        TELEGRAM_TOKEN = credentials('TELEGRAM_TOKEN') // Retrieve Telegram bot token from Jenkins credentials store
    }

    agent {
        docker {
            image 'beny14/dockerfile_agent:latest' // Use the Docker image 'beny14/dockerfile_agent:latest' for the build agent
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock' // Pass Docker-in-Docker setup arguments for the agent
        }
    }

    stages {
        stage('Build') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_key', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        try {
                            echo "Starting Docker build" // Log message indicating the start of the Docker build process
                            sh """
                                echo ${USERPASS} | docker login -u ${USERNAME} --password-stdin # Log in to Docker registry using credentials
                                docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} . # Build Docker image with the tag of build number
                                docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${DOCKER_REPO}:latest # Tag the Docker image as 'latest'
                                docker push ${DOCKER_REPO}:${BUILD_NUMBER} # Push the Docker image tagged with the build number to the repository
                                docker push ${DOCKER_REPO}:latest # Push the Docker image tagged 'latest' to the repository
                            """
                            foo() // Call a function named 'foo' from the shared library
                            echo "Docker build and push completed" // Log message indicating the completion of the Docker build and push
                        } catch (Exception e) {
                            error "Build failed: ${e.getMessage()}" // Log error message if the build fails
                        }
                    }
                }
            }
        }

        stage('Unit Test') {
            steps {
                script {
                    echo "Starting Unit Tests" // Log message indicating the start of unit tests
                    docker.image("${DOCKER_REPO}:${BUILD_NUMBER}").inside {
                        sh """
                        python3 -m venv venv # Create a Python virtual environment
                        . venv/bin/activate # Activate the virtual environment
                        pip install --upgrade pip # Upgrade pip to the latest version
                        pip install -r requirements.txt # Install project dependencies from requirements.txt
                        pip install pytest-xdist pytest-timeout # Install pytest plugins for parallel test execution and timeout
                        python3 -m pytest -n 4 --timeout=60 --junitxml results.xml tests/*.py # Run unit tests with concurrency and timeout, saving results to XML
                        deactivate # Deactivate the virtual environment
                        """
                    }
                    echo "Unit Tests completed" // Log message indicating the completion of unit tests
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'results.xml' // Archive unit test results for Jenkins, allowing empty results
                }
            }
        }

        stage('Lint Test') {
            steps {
                script {
                    try {
                        echo "Starting Lint Tests" // Log message indicating the start of lint tests
                        docker.image("${DOCKER_REPO}:${BUILD_NUMBER}").inside {
                            sh '''
                            python3 -m venv venv # Create a Python virtual environment
                            . venv/bin/activate # Activate the virtual environment
                            pylint --disable=E1136,C0301,C0114,E1101,C0116,C0103,W0718,E0401,W0613,R1722,W0612,R0912,C0304,C0115,R1705 polybot/*.py > pylint.log || true # Run lint checks and save output to pylint.log, allowing the command to succeed even with linting issues
                            ls -alh # List files to verify presence
                            cat pylint.log # Display the content of the pylint log file
                            deactivate # Deactivate the virtual environment
                            '''
                        }
                        echo "Lint Tests completed" // Log message indicating the completion of lint tests
                    } catch (Exception e) {
                        error "Test failed: ${e.getMessage()}" // Log error message if lint tests fail
                    }
                }
            }
            post {
                always {
                    script {
                        try {
                            archiveArtifacts artifacts: 'pylint.log', allowEmptyArchive: true # Archive the pylint log file, allowing empty archive if the file is missing
                            echo "Pylint log content:" // Log message before displaying pylint log content
                            sh 'cat pylint.log' # Display the pylint log content
                        } catch (Exception e) {
                            echo "Archiving or recording issues failed: ${e.getMessage()}" # Log error if archiving or displaying the log fails
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Cleaning up Docker containers and images" // Log message indicating the start of Docker cleanup
                def containerId = sh(script: "docker ps -q -f ancestor=${DOCKER_REPO}:${BUILD_NUMBER}", returnStdout: true).trim() // Get the container ID for the current build image

                sh """
                    for id in \$(docker ps -a -q -f ancestor=${DOCKER_REPO}:${BUILD_NUMBER}); do
                        if [ "\$id" != "${containerId}" ]; then
                            docker rm -f \$id || true # Remove old containers except the current build container
                        fi
                    done
                """
                sh """
                    docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | grep '${DOCKER_REPO}' | grep -v ':latest' | grep -v ':${BUILD_NUMBER}' | awk '{print \$2}' | xargs --no-run-if-empty docker rmi -f || true # Remove old Docker images except 'latest' and the current build image
                """
                cleanWs() // Clean the Jenkins workspace directory
                echo "Cleanup completed" // Log message indicating the completion of cleanup
            }
        }

        failure {
            script {
                def errorMessage = currentBuild.result == 'FAILURE' ? currentBuild.description : 'Build failed' // Determine the error message based on the build result
                echo "Error occurred: ${errorMessage}" // Log error message if the build fails
            }
        }
    }
}
