pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        APP_PORT = "8005"

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
                pip install --upgrade pip
                pip install --no-cache-dir -r requirements.txt
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
           Stage 8: Parallel Pytests (Unit + API)
        ================================= */
        stage("Run Pytests") {
            parallel {
                stage("Unit Tests") {
                    steps {
                        sh '''
                        . $VENV_NAME/bin/activate
                        export PYTHONPATH=$(pwd)
                        pytest test_data.py
                        pytest test_model.py
                        '''
                    }
                }
                stage("API & Schema Tests") {
                    steps {
                        sh '''
                        . $VENV_NAME/bin/activate
                        export PYTHONPATH=$(pwd)
                        pytest test_api.py
                        pytest test_schema.py -W ignore::pydantic.PydanticDeprecatedSince20
                        '''
                    }
                }
            }
        }

        /* ================================
           Stage 9: Schema Validation
        ================================= */
        stage("Schema Validation") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                export PYTHONPATH=$(pwd)
                python schema.py
                '''
            }
        }

        /* ================================
           Stage 10: FastAPI Smoke Test
        ================================= */
        stage("FastAPI Smoke Test") {
            steps {
                sh '''#!/bin/bash
                set -euo pipefail
                . $VENV_NAME/bin/activate
                export PYTHONPATH=$WORKSPACE

                echo "🚀 Starting FastAPI..."
                nohup uvicorn main:app --host 0.0.0.0 --port $APP_PORT > uvicorn.log 2>&1 &
                UVICORN_PID=$!

                echo "⏳ Waiting for FastAPI..."
                i=0
                while [ $i -lt 20 ]; do
                  if curl -s http://localhost:$APP_PORT/health | grep -q ok; then
                    echo "✅ FastAPI is up"
                    break
                  fi
                  sleep 1
                  i=$((i+1))
                done

                if ! curl -s http://localhost:$APP_PORT/health | grep -q ok; then
                  echo "❌ FastAPI failed to start"
                  cat uvicorn.log
                  kill $UVICORN_PID || true
                  exit 1
                fi

                echo "📡 Testing /predict..."
                # Generate JSON from schema to avoid 422
                PRED_JSON=$(python -c "from schema import FraudInputSchema; import json; print(json.dumps(FraudInputSchema().model_dump()))")
                curl -f http://localhost:$APP_PORT/predict -H "Content-Type: application/json" -d "$PRED_JSON"

                # Cleanup
                kill $UVICORN_PID
                '''
            }
        }

        /* ================================
           Stage 11: Docker Build & Run
        ================================= */
        stage("Docker Build & Run") {
            steps {
                sh '''#!/bin/bash
                set -euo pipefail

                OLD_ID=$(docker ps -aq --filter "name=credit-card-fraud")
                if [ -n "$OLD_ID" ]; then
                  docker rm -f $OLD_ID || true
                fi

                docker rmi -f credit-card-fraud || true

                docker build -t credit-card-fraud .
                HOST_PORT=$(shuf -i 8000-8999 -n 1)
                echo $HOST_PORT > .docker_port

                CONTAINER_ID=$(docker run -d -p $HOST_PORT:8005 --name credit-card-fraud credit-card-fraud)
                echo $CONTAINER_ID > .docker_container_id

                echo "🐳 Docker running"
                echo "🆔 Container ID: $CONTAINER_ID"
                echo "🌐 Port: $HOST_PORT"
                '''
            }
        }

        /* ================================
           Stage 12: FastAPI Docker Test
        ================================= */
        stage("FastAPI Docker Test") {
            steps {
                sh '''#!/bin/bash
                set -euo pipefail

                HOST_PORT=$(cat .docker_port)
                CONTAINER_ID=$(cat .docker_container_id)

                echo "⏳ Waiting for Docker FastAPI on port $HOST_PORT..."
                i=0
                while [ $i -lt 30 ]; do
                  if curl -s http://localhost:$HOST_PORT/health | grep -q ok; then
                    echo "✅ Docker API is up"
                    break
                  fi
                  sleep 1
                  i=$((i+1))
                done

                # Generate valid JSON for prediction
                PRED_JSON=$(python -c "from schema import FraudInputSchema; import json; print(json.dumps(FraudInputSchema().model_dump()))")
                curl -f -s http://localhost:$HOST_PORT/predict -H "Content-Type: application/json" -d "$PRED_JSON"

                # Cleanup
                docker rm -f $CONTAINER_ID
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
