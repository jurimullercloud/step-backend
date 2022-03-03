pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS=credentials('dockerhub-access')
    }

    stages {
        stage ("Install Dependencies") {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage ("Run Tests") {
            steps {
                script {
                    env.RUNNING_ENV = "TEST"
                }
                sh 'python3 run_tests.py'
            }
        }

        stage ("Create Build Wheel") {
           steps {
                sh 'python3 setup.py bdist_wheel'
           }
        }

        stage ("Build Docker Image") {
            steps {
                sh 'docker build -t ${REGISTRY_NAME}/${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }

        stage ("Login to Dockerhub") {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
            }
        }

        stage ("Push new Image to Dockerhub") {
            steps {
                sh 'docker push ${REGISTRY_NAME}/${IMAGE_NAME}:${IMAGE_TAG}'
            }
        }
    }

}