
pipeline {


   agent any

   stages {
      stage('Unittest'){
         steps{
            sh 'echo "testing"'
          }
      }
      stage('Lint') {
         steps {
             sh '''
             cd polybot
             pip install -r requirements.txt
             python3 -m plint *.py
                '''
         }
      }

      stage('Functional test') {
         steps {
             sh 'echo "testing "'
         }
      }



   }
}
