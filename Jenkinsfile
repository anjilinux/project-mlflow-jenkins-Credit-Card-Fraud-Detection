pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        APP_PORT = "8005"

        // Safer for CI (no external dependency)
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "credit-card-fraud"
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
    }

    stages {

        /* ================================
           Stage 1: Checkout Code
        ================================= */
        stage("Checkout Code") {
            steps {
                git branch: "master",
                    url: "https://github.com/anjilinux/project-mlflow-jenkins-Credit-Card-Fraud-Detection.git"
            }
        }

        /* ================================
           Stage 2: Setup Virtual Environment
        ================================= */
        stage("Setup Virtual Environment") {
            steps {
                sh '''
                
                python3 -m venv $VENV_NAME
                . $VENV_NAME/bin/activate

                pip install -r requirements.txt
                '''
            }
        }

        /* ================================
           Stage 3: Data Ingestion
        ================================= */
        stage("Data Ingestion") {
            steps {
                sh '''
                
                . $VENV_NAME/bin/activate
                python data_ingestion.py
                '''
            }
        }

        /* ================================
           Stage 4: Feature Engineering
        ================================= */
        stage("Feature Engineering") {
            steps {
                sh '''
                
                . $VENV_NAME/bin/activate
                python feature_engineering.py
                '''
            }
        }

        /* ================================
           Stage 5: Data Preprocessing
        ================================= */
        stage("Data Preprocessing") {
            steps {
                sh '''

                . $VENV_NAME/bin/activate
                python preprocessing.py
                '''
            }
        }

        /* ================================
           Stage 6: Model Training (MLflow)
        ================================= */
        stage("Model Training") {
            steps {
                sh '''
                
                . $VENV_NAME/bin/activate
                export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                export MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
                python train.py
                '''
            }
        }

        /* ================================
           Stage 7: Model Evaluation
        ================================= */
        stage("Model Evaluation") {
            steps {
                sh '''
                
                . $VENV_NAME/bin/activate
                python evaluate.py
                '''
            }
        }

        /* ================================
           Stage 8: Pytests (Unit + API)
        ================================= */
        stage("Run Pytests") {
            steps {
                sh '''
                
                . $VENV_NAME/bin/activate
                 

                pytest tests/test_data.py
                pytest tests/test_model.py
                pytest tests/test_api.py
                pytest test_schema.py
                '''
            }
        }

        /* ================================
           Stage 9: Schema Validation
        ================================= */
        stage("Schema Validation") {
            steps {
                sh '''
                
                . $VENV_NAME/bin/activate
                 

                pytest test_schema.py
                '''
            }
        }

        /* ================================
           Stage 10: FastAPI Local Smoke Test
        ================================= */
        stage("FastAPI Smoke Test") {
            steps {
                sh '''
                set -e
                . $VENV_NAME/bin/activate
                 

                nohup uvicorn app.main:app \
                  --host 0.0.0.0 \
                  --port $APP_PORT > uvicorn.log 2>&1 &

                API_PID=$!

                for i in {1..30}; do
                    if curl -s http://localhost:$APP_PORT/health | grep -q "ok"; then
                        break
                    fi
                    sleep 1
                done

                curl -s -X POST http://localhost:$APP_PORT/predict \
                  -H "Content-Type: application/json" \
                  -d '{
                    "V1":0.1,"V2":0.1,"V3":0.1,"V4":0.1,"V5":0.1,
                    "V6":0.1,"V7":0.1,"V8":0.1,"V9":0.1,"V10":0.1,
                    "V11":0.1,"V12":0.1,"V13":0.1,"V14":0.1,"V15":0.1,
                    "V16":0.1,"V17":0.1,"V18":0.1,"V19":0.1,"V20":0.1,
                    "V21":0.1,"V22":0.1,"V23":0.1,"V24":0.1,"V25":0.1,
                    "V26":0.1,"V27":0.1,"V28":0.1,"Amount":0.5
                  }'

                kill $API_PID
                '''
            }
        }

        /* ================================
           Stage 11: Docker Build & Run
        ================================= */
        stage("Docker Build & Run") {
            steps {
                sh '''
                
                docker build -t credit-card-fraud .
                docker rm -f credit-card-fraud || true

                HOST_PORT=$(shuf -i 8000-8999 -n 1)
                docker run -d -p $HOST_PORT:$APP_PORT \
                  --name credit-card-fraud credit-card-fraud

                echo $HOST_PORT > .docker_port
                '''
            }
        }

        /* ================================
           Stage 12: Docker API Test
        ================================= */
        stage("FastAPI Docker Test") {
            steps {
                sh '''
                
                HOST_PORT=$(cat .docker_port)

                for i in {1..30}; do
                    if curl -s http://localhost:$HOST_PORT/health | grep -q "ok"; then
                        break
                    fi
                    sleep 1
                done

                curl -s -X POST http://localhost:$HOST_PORT/predict \
                  -H "Content-Type: application/json" \
                  -d '{
                    "V1":0.1,"V2":0.1,"V3":0.1,"V4":0.1,"V5":0.1,
                    "V6":0.1,"V7":0.1,"V8":0.1,"V9":0.1,"V10":0.1,
                    "V11":0.1,"V12":0.1,"V13":0.1,"V14":0.1,"V15":0.1,
                    "V16":0.1,"V17":0.1,"V18":0.1,"V19":0.1,"V20":0.1,
                    "V21":0.1,"V22":0.1,"V23":0.1,"V24":0.1,"V25":0.1,
                    "V26":0.1,"V27":0.1,"V28":0.1,"Amount":0.5
                  }'

                docker rm -f credit-card-fraud
                '''
            }
        }

        /* ================================
           Stage 13: Archive Artifacts
        ================================= */
        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: '''
                    model.pkl,
                    mlruns/**,
                    uvicorn.log
                ''', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Credit Card Fraud MLOps Pipeline Completed Successfully"
        }
        failure {
            echo "❌ Pipeline Failed – Check Jenkins Logs"
        }

    }
}
