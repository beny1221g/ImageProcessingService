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
                    def buildNumber = params.BUILD_NUMBER ? params.BUILD_NUMBER : 'latest'
                    def dockerImage = "${params.IMAGE_NAME}:${buildNumber}"
                    echo "Starting build and push of Docker image ${dockerImage}"
                    sh """
                        docker login localhost:8083
                        docker tag ${dockerImage} localhost:8083/${dockerImage}
                        docker push localhost:8083/${dockerImage}
                    """
                    echo "Docker push to Nexus completed successfully"
                }
            }
        }

        stage('Update Project and Restart Services') {
            steps {
                script {
                    echo "Updating project and restarting Docker services"

                    // Ensure proper permissions
                    sh """
                        sudo chmod -R 775 /project_poly
                    """

                    // Pull the latest changes from the Git repository
                    sh """
                        cd /project_poly
                        git config --global --add safe.directory /project_poly
                        git pull https://github.com/beny1221g/ImageProcessingService.git
                    """

                    // Stop and remove existing containers
                    sh """
                        docker-compose down
                    """

                    // Start updated containers
                    sh """
                        docker-compose up -d
                    """

                    echo "Project updated and containers restarted successfully"
                }
            }
        }
    }
}
