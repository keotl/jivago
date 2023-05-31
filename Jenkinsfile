pipeline {
    agent none
    stages {
	matrix {
	    agent {
		kubernetes {
		    yaml """
apiVersion: v1
kind: Pod
metadata:
  name: python
spec:
  containers:
  - name: python
    image: python:${PYTHON_VERSION}
"""
		}
	    }
            axes {
                axis {
                    name 'PYTHON_VERSION'
                    values '3.10', '3.9', '3.8', '3.7', '3.6'
                }
            }
	    stages {
		stage('Install dependencies') {
		    steps {
			checkout scm
			sh 'pip install -r requirements.txt'
		    }
		}
		stage('Test') {
		    steps {
			sh 'sh run_tests.sh'
			sh 'sh run_e2e_tests.sh'
		    }
		}
	    }
	}
    }
}
