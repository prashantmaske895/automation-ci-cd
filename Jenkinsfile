pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t playwright-framework .'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                mkdir -p automation/reports

                docker run --rm \
                  -v $WORKSPACE/automation/reports:/app/automation/reports \
                  playwright-framework
                '''
            }
        }
    }

    post {

        always {

            archiveArtifacts artifacts: 'automation/reports/**', fingerprint: true

            junit 'automation/reports/results.xml'
        }

        success {
            echo 'Playwright tests completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}