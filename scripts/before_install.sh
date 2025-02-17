#!/bin/bash
DIR="/home/ec2-user/fastapi-app"
if [ -d "$DIR" ]; then
  rm -rf ${DIR}
  echo "${DIR} exists"
else
  echo "Creating ${DIR} directory"
  sudo mkdir ${DIR}
  # Definir permissões
  sudo chown -R ec2-user:ec2-user ${DIR}
fi