#!/bin/bash

ENV_CONFIG="${1:-dev}"

if [ "$ENV_CONFIG" == "dev" ]; then
    echo "Running in Development mode"
    waitress-serve --port=8080 wsgi:app

elif [ "$ENV_CONFIG" == "prod" ]; then
    echo "Running in Production mode"
    export FLASK_ENV=Production
    waitress-serve --port=8080 wsgi:app

elif [ "$ENV_CONFIG" == "test" ]; then
    echo "Running Test"
    pytest

else
    echo "Unknown environment: $ENV_CONFIG"
    exit 1
fi