
cd lambda
uv sync
uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt
uv pip install -r requirements.txt --target package

cd infra
cdk deploy --all

check event approval status for each attendee
