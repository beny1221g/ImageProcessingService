pipeline {
    agent any

    parameters {
        string(name: 'IMAGE_NAME', defaultValue: 'beny14/polybot', description: 'Name of the Docker image')
        string(name: 'BUILD_NUMBER', defaultValue: '', description: 'Build number of the Docker image to deploy')
    }

    stages {
        stage('Build and Push Docker Image to Nexus') {
            steps {
                script {
                    def dockerImage = "${params.IMAGE_NAME}:${params.BUILD_NUMBER}"
                    echo "Starting build and push of Docker image ${dockerImage}"
                    sh """
                        docker build -t ${dockerImage} .
                        echo $NEXUS_PASS | docker login localhost:8083 -u $NEXUS_USER --password-stdin
                        docker push localhost:8083/${dockerImage}
                    """
                    echo "Docker push to Nexus completed"
                }
            }
        }
    }
}
