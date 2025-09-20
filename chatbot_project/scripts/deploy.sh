#!/bin/bash
set -e

echo ">>> Logging in to ECR..."
aws ecr get-login-password --region ap-south-1 \
 | docker login --username AWS --password-stdin 959305806189.dkr.ecr.ap-south-1.amazonaws.com

echo ">>> Pulling latest image..."
docker pull 959305806189.dkr.ecr.ap-south-1.amazonaws.com/chatbot:latest

cd /home/ubuntu/chatbot_app/chatbot_project

echo ">>> Restarting containers..."
docker compose down || true
docker compose up -d
