pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Tag to be applied to the Docker image')
    }

    stages {
        stage('Push Docker Image to Nexus') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "nexus_user", usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                        try {
                            def dockerImage = "beny14/polybot"
                            def taggedImage = "${dockerImage}:${params.IMAGE_TAG}"
                            echo "Starting Docker push to Nexus with tag ${params.IMAGE_TAG}"
                            sh """
                                echo $NEXUS_PASS | docker login localhost:8083 -u $NEXUS_USER --password-stdin
                                docker push localhost:8083/${taggedImage}
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
