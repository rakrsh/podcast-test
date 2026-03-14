pipeline {
    agent any

    environment {
        POETRY_HOME = "${WORKSPACE}/.poetry"
        PATH = "${POETRY_HOME}/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Poetry') {
            steps {
                sh '''
                curl -sSL https://install.python-poetry.org | python3 -
                export PATH="$HOME/.local/bin:$PATH"
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                poetry install --with dev,test
                '''
            }
        }

        stage('Lint and Style Check') {
            steps {
                sh '''
                poetry run pre-commit run --all-files
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                poetry run pytest tests --cov=.
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                poetry run pip install bandit
                poetry run bandit -r .
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${env.JENKINS_REPO}:latest")
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.DOCKERHUB_USERNAME && env.DOCKERHUB_TOKEN }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                    echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
                    docker tag ${env.JENKINS_REPO}:latest $DOCKERHUB_USERNAME/podcast-test:latest
                    docker push $DOCKERHUB_USERNAME/podcast-test:latest
                    '''
                }
            }
        }
    }
}
