pipeline {
    agent any

    parameters {
        string(name: 'DOCKER_IMAGE', defaultValue: 'beny14/polybot:latest', description: 'Docker Image to build and push')
    }

    environment {
        DOCKER_REPO = "beny14/polybot"
        NEXUS_CREDENTIAL = credentials('nexus_user') // Replace with your Nexus credentials ID
        NEXUS_REPO_URL = "http://192.168.1.75:5000/repository/docker-repo/" // Replace  with your Nexus repository URL
    }

    stages {
        stage('Build and Push Docker Image to Nexus') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "nexus_credentials_id", usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                        try {
                            echo "Starting Docker build and push to Nexus"
                            sh """
                                echo ${NEXUS_PASS} | docker login -u ${NEXUS_USER} --password-stdin ${NEXUS_REPO_URL}
                                docker pull ${DOCKER_IMAGE}
                                docker tag ${DOCKER_IMAGE} ${DOCKER_REPO}:latest
                                docker push ${DOCKER_REPO}:latest
                            """
                            echo "Docker build and push to Nexus completed"
                        } catch (Exception e) {
                            error "Build and push to Nexus failed: ${e.getMessage()}"
                        }
                    }
                }
            }
        }
    }
}
