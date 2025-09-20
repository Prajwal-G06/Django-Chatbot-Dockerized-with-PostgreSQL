#!/bin/bash
set -e

REGION="ap-south-1"
ACCOUNT_ID="<YOUR_AWS_ACCOUNT_ID>"
ECR_REPO="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/chatbot"

echo ">>> Fetching parameters from SSM Parameter Store..."
PARAMS=$(aws ssm get-parameters-by-path \
  --path "/chatbot/" \
  --region $REGION \
  --with-decryption \
  --query "Parameters[*].[Name,Value]" \
  --output text)

echo ">>> Exporting environment variables..."
while read -r name value; do
  key=$(basename "$name")
  export "$key=$value"
done <<< "$PARAMS"

echo ">>> Logging in to Amazon ECR..."
aws ecr get-login-password --region $REGION \
  | docker login --username AWS --password-stdin $ECR_REPO

echo ">>> Pulling latest Docker image..."
docker pull $ECR_REPO:latest

cd /home/ubuntu/chatbot_app/chatbot_project

echo ">>> Restarting containers with new environment..."
docker compose down || true
docker compose up -d

echo ">>> Deployment complete!"
