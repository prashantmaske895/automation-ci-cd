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
          -v ${WORKSPACE}/automation/reports:/app/automation/reports \
          playwright-framework

        echo "===== Jenkins Workspace ====="
        pwd

        echo "===== Reports Directory ====="
        ls -la automation/reports || true

        echo "===== Find Reports ====="
        find . -name "*.html"
        find . -name "*.xml"
        '''
    }
}
    }

    post {
    always {
        archiveArtifacts artifacts: 'automation/reports/**', allowEmptyArchive: true
        junit testResults: 'automation/reports/results.xml', allowEmptyResults: true
    }

    success {
        echo 'Playwright tests completed successfully.'
    }

    failure {
        echo 'Pipeline failed.'
    }
}
}