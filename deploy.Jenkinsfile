pipeline {
    agent any

    parameters {
        string(name: 'DOCKER_IMAGE', defaultValue: 'beny14/polybot:latest', description: 'Docker Image to build and push')
    }

    stages {
        stage('Build and Push Docker Image to Nexus') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "nexus_credentials_id", usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                        try {
                            echo "Starting Docker build and push to Nexus"
                            sh """
                                echo $NEXUS_PASS | docker login localhost:8083 -u $NEXUS_USER --password-stdin
                                docker push localhost:8083/${params.DOCKER_IMAGE}
                            """
                            echo "Docker push to Nexus completed"
                        } catch (Exception e) {
                            error "Build and push to Nexus failed: ${e.getMessage()}"
                        }
                    }
                }
            }
        }
    }
}