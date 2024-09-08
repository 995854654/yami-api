#! /bin/bash

APP_NAME="yami-api"
APP_VERSION="latest"
DOCKER_FILE="cicd/Dockerfile"

docker build -f $DOCKER_FILE \
             -t $APP_NAME:$APP_VERSION .