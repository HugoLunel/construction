set -e
set -o pipefail

docker build -t construction . --progress=plain

AWS_REGION=$(aws configure get region)
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)

docker run \
  -e AWS_REGION=$AWS_REGION \
  -e AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
  -p 9000:8080 \
  --rm \
  construction:latest

# curl.exe -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{}"