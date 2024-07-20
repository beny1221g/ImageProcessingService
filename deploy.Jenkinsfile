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

                    // Check and switch to the main branch if necessary
                    sh """
                        pwd
                        cd /
                        cd /project_poly
                        git fetch
                        current_branch=\$(git branch --show-current)
                        if [ "\$current_branch" != "main" ]; then
                            if git show-ref --quiet refs/heads/main; then
                                echo "Switching to the 'main' branch."
                                git checkout main
                            else
                                if git show-ref --quiet refs/heads/master; then
                                    echo "Renaming 'master' branch to 'main' and switching to it."
                                    git branch -m master main
                                    git checkout main
                                else
                                    echo "'main' branch does not exist and 'master' branch is not found to rename."
                                    exit 1
                                fi
                            fi
                        else
                            echo "You are already on the 'main' branch."
                        fi
                    """

                    // Pull the latest changes from the Git repository
                    sh """
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
