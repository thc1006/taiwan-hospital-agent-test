# hospital-agent-sam-python-skeleton

> Minimal, deployable skeleton for a "醫院分診 & 人力調度 Agent" backend on AWS using **SAM + Lambda + API Gateway + Bedrock (Converse & Knowledge Bases)**. Includes IaC, Lambda handler, RAG ingestion script, and pytest.

---

## Project layout
```
hospital-agent-sam-python-skeleton/
├─ template.yaml
├─ Makefile
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ src/
│  ├─ app.py
│  ├─ bedrock_clients.py
│  ├─ config.py
│  └─ __init__.py
├─ rag/
│  └─ ingest.py
└─ tests/
   └─ test_app.py
```

---

## template.yaml (AWS SAM)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Minimal hospital agent API (Python + Bedrock + Knowledge Bases)

Globals:
  Function:
    Runtime: python3.12
    Timeout: 30
    MemorySize: 1024
    Tracing: Active

Parameters:
  ModelId:
    Type: String
    Default: anthropic.claude-3-sonnet-20240229-v1:0
    Description: Bedrock model ID for Converse (adjust per region availability)
  KnowledgeBaseId:
    Type: String
    Default: ""
    Description: (Optional) Bedrock Knowledge Base ID (for RAG)
  DataSourceId:
    Type: String
    Default: ""
    Description: (Optional) Data Source ID attached to the Knowledge Base
  GuardrailIdentifier:
    Type: String
    Default: ""
    Description: (Optional) Guardrail ID or ARN
  BedrockRegion:
    Type: String
    Default: ap-southeast-1
    Description: Region where Bedrock is enabled for your account
  KbDocsBucketName:
    Type: String
    Description: S3 bucket name to store raw documents for Knowledge Base ingestion

Resources:
  Api:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: prod

  ApiHandler:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: app.lambda_handler
      Description: HTTP API → Lambda (Proxy). Routes to Converse or KB RAG
      Environment:
        Variables:
          MODEL_ID: !Ref ModelId
          KB_ID: !Ref KnowledgeBaseId
          KB_DS_ID: !Ref DataSourceId
          GUARDRAIL_ID: !Ref GuardrailIdentifier
          BEDROCK_REGION: !Ref BedrockRegion
          DOCS_BUCKET: !Ref KbDocsBucketName
      Policies:
        - AWSLambdaBasicExecutionRole
        - Statement:
            - Effect: Allow
              Action:
                - bedrock:InvokeModel
                - bedrock:InvokeModelWithResponseStream
                - bedrock:ApplyGuardrail
              Resource: "*"
            - Effect: Allow
              Action:
                - bedrock:Retrieve
                - bedrock:RetrieveAndGenerate
              Resource: "*"
            - Effect: Allow
              Action:
                - bedrock:StartIngestionJob
                - bedrock:GetIngestionJob
                - bedrock:ListDataSources
              Resource: "*"
            - Effect: Allow
              Action:
                - s3:GetObject
                - s3:PutObject
                - s3:ListBucket
              Resource:
                - !Sub arn:aws:s3:::${KbDocsBucketName}
                - !Sub arn:aws:s3:::${KbDocsBucketName}/*
            - Effect: Allow
              Action:
                - secretsmanager:GetSecretValue
              Resource: "*"
      Events:
        Proxy:
          Type: HttpApi
          Properties:
            ApiId: !Ref Api
            Method: ANY
            Path: /{proxy+}

  KbDocsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref KbDocsBucketName

Outputs:
  ApiEndpoint:
    Description: HTTP API endpoint base URL
    Value: !Sub "https://${Api}.execute-api.${AWS::Region}.amazonaws.com/prod"
```

---

## Makefile
```make
.PHONY: venv deps build deploy delete local test fmt

venv:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip

deps: venv
	. .venv/bin/activate && pip install -r requirements.txt

build:
	sam build

deploy:
	sam deploy --guided

local:
	sam local start-api

test:
	. .venv/bin/activate && pytest -q

delete:
	sam delete

fmt:
	python -m pip install ruff && ruff format
```

---

## requirements.txt
```
boto3
botocore
pytest
```

---

## src/config.py
```python
import os
import json
import boto3
from botocore.exceptions import ClientError

MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
GUARDRAIL_ID = os.getenv("GUARDRAIL_ID", "")
KB_ID = os.getenv("KB_ID", "")
KB_DS_ID = os.getenv("KB_DS_ID", "")
DOCS_BUCKET = os.getenv("DOCS_BUCKET", "")

_secrets = boto3.client("secretsmanager")

def get_secret(name: str) -> dict:
    """Retrieve a secret from AWS Secrets Manager as dict."""
    try:
        resp = _secrets.get_secret_value(SecretId=name)
        sec = resp.get("SecretString") or resp.get("SecretBinary")
        if isinstance(sec, (bytes, bytearray)):
            sec = sec.decode("utf-8")
        return json.loads(sec) if sec else {}
    except ClientError as e:
        # For skeleton: log and return empty; production should raise/handle properly
        print(f"SecretsManager error for {name}: {e}")
        return {}
```

---

## src/bedrock_clients.py
```python
import boto3
from . import config

def bedrock_runtime():
    return boto3.client("bedrock-runtime", region_name=config.BEDROCK_REGION)

def bedrock_agent_runtime():
    return boto3.client("bedrock-agent-runtime", region_name=config.BEDROCK_REGION)
```

---

## src/app.py
```python
import json
from typing import Any, Dict
from . import config
from .bedrock_clients import bedrock_runtime, bedrock_agent_runtime


def _response(status: int, body: Dict[str, Any]):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, ensure_ascii=False),
    }


def _converse(prompt: str) -> str:
    brt = bedrock_runtime()
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    kwargs: Dict[str, Any] = {
        "modelId": config.MODEL_ID,
        "messages": messages,
        "inferenceConfig": {"maxTokens": 1024},
    }
    # Optional Guardrail
    if config.GUARDRAIL_ID:
        kwargs["guardrailConfiguration"] = {
            "guardrailIdentifier": config.GUARDRAIL_ID,
            "guardrailVersion": "DRAFT",
        }
    resp = brt.converse(**kwargs)
    parts = resp.get("output", {}).get("message", {}).get("content", [])
    text = "".join([p.get("text", "") for p in parts if "text" in p])
    return text


def _kb_query(query: str) -> Dict[str, Any]:
    if not config.KB_ID:
        return {"answer": "Knowledge base not configured.", "citations": []}
    ar = bedrock_agent_runtime()
    # Note: Depending on SDK version, pass model info as modelArn or inferenceProfile
    out = ar.retrieve_and_generate(
        input={"text": query},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": config.KB_ID,
                # If your SDK expects modelArn, construct from region + modelId
                # Example: arn:aws:bedrock:REGION::foundation-model/MODEL_ID
                # "modelArn": f"arn:aws:bedrock:{config.BEDROCK_REGION}::foundation-model/{config.MODEL_ID}",
            },
        },
    )
    answer = out.get("output", {}).get("text", "")
    citations = []
    for c in out.get("citations", []):
        for ref in c.get("retrievedReferences", []):
            citations.append({
                "content": ref.get("content", {}).get("text", ""),
                "location": ref.get("location", {}),
            })
    return {"answer": answer, "citations": citations}


def lambda_handler(event, context):
    path = event.get("rawPath") or event.get("path", "/")
    method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod")

    if method == "POST" and path.endswith("/triage"):
        try:
            body = json.loads(event.get("body") or "{}")
            prompt = body.get("prompt") or "請根據院內規範提供分診與人力建議。"
            text = _converse(prompt)
            return _response(200, {"result": text})
        except Exception as e:
            return _response(500, {"error": str(e)})

    if method == "POST" and path.endswith("/kb/query"):
        try:
            body = json.loads(event.get("body") or "{}")
            q = body.get("query") or "院內SOP查詢"
            res = _kb_query(q)
            return _response(200, res)
        except Exception as e:
            return _response(500, {"error": str(e)})

    return _response(404, {"message": f"Not found: {method} {path}"})
```

---

## rag/ingest.py
```python
"""Upload local files to S3 and trigger Knowledge Base ingestion.

Usage:
  export AWS_REGION=ap-southeast-1
  export DOCS_BUCKET=your-bucket
  export KB_ID=kb-xxxxxxxx
  export KB_DS_ID=ds-xxxxxxxx
  python rag/ingest.py ./docs
"""

import os
import sys
import time
import pathlib
import boto3

REGION = os.getenv("AWS_REGION") or os.getenv("BEDROCK_REGION", "us-east-1")
BUCKET = os.getenv("DOCS_BUCKET", "")
KB_ID = os.getenv("KB_ID", "")
DS_ID = os.getenv("KB_DS_ID", "")

s3 = boto3.client("s3", region_name=REGION)
agent = boto3.client("bedrock-agent", region_name=REGION)

def upload_dir(src: str):
    base = pathlib.Path(src)
    for p in base.rglob("*"):
        if p.is_file():
            key = str(p.relative_to(base)).replace("\\", "/")
            print(f"Uploading {p} to s3://{BUCKET}/{key}")
            s3.upload_file(str(p), BUCKET, key)


def start_ingestion():
    print("Starting ingestion job…")
    resp = agent.start_ingestion_job(knowledgeBaseId=KB_ID, dataSourceId=DS_ID)
    job = resp.get("ingestionJob", {})
    jid = job.get("ingestionJobId")
    print("Job:", jid)
    return jid


def wait_job(jid: str):
    while True:
        desc = agent.get_ingestion_job(knowledgeBaseId=KB_ID, dataSourceId=DS_ID, ingestionJobId=jid)
        st = desc.get("ingestionJob", {}).get("status")
        print("Status:", st)
        if st in {"SUCCEEDED", "FAILED", "CANCELED"}:
            return st
        time.sleep(10)


def main():
    if not (BUCKET and KB_ID and DS_ID):
        print("Set DOCS_BUCKET, KB_ID and KB_DS_ID env vars.")
        sys.exit(2)
    src = sys.argv[1] if len(sys.argv) > 1 else "./docs"
    upload_dir(src)
    jid = start_ingestion()
    st = wait_job(jid)
    print("Ingestion finished:", st)

if __name__ == "__main__":
    main()
```

---

## tests/test_app.py
```python
import json
from src import app


def test_not_found():
    event = {"rawPath": "/", "requestContext": {"http": {"method": "GET"}}}
    res = app.lambda_handler(event, None)
    assert res["statusCode"] == 404


def test_converse_route_smoke(monkeypatch):
    class Dummy:
        def converse(self, **kwargs):
            return {"output": {"message": {"content": [{"text": "ok"}]}}}
    monkeypatch.setattr(app, "bedrock_runtime", lambda: Dummy())
    ev = {"rawPath": "/triage", "requestContext": {"http": {"method": "POST"}}, "body": json.dumps({"prompt": "hi"})}
    res = app.lambda_handler(ev, None)
    assert res["statusCode"] == 200
    assert json.loads(res["body"]) == {"result": "ok"}


def test_kb_route_smoke(monkeypatch):
    class Dummy:
        def retrieve_and_generate(self, **kwargs):
            return {"output": {"text": "kb"}, "citations": []}
    monkeypatch.setattr(app, "bedrock_agent_runtime", lambda: Dummy())
    ev = {"rawPath": "/kb/query", "requestContext": {"http": {"method": "POST"}}, "body": json.dumps({"query": "hi"})}
    res = app.lambda_handler(ev, None)
    assert res["statusCode"] == 200
    assert json.loads(res["body"]) == {"answer": "kb", "citations": []}
```

---

## README.md (quick start)
```markdown
# Hospital Agent – Minimal SAM + Lambda + Bedrock (Python)

## Prerequisites
- AWS CLI & credentials with appropriate permissions
- AWS SAM CLI
- Docker (for `sam local`)
- Python 3.12

## Configure
Set parameters at deploy time (recommended) or as env vars for local tests:
- `MODEL_ID` (e.g., anthropic.claude-3-sonnet-20240229-v1:0)
- `BEDROCK_REGION` (e.g., ap-southeast-1)
- `KB_ID`, `KB_DS_ID` (when using Knowledge Bases)
- `DOCS_BUCKET` (S3 bucket for your raw docs)

## Install & Test
```bash
make deps
make test
```

## Run locally
```bash
make local
# Invoke
curl -s -X POST http://127.0.0.1:3000/triage -d '{"prompt": "請提供分診與人力建議"}' -H 'Content-Type: application/json'
```

## Deploy
```bash
make build
make deploy   # first time will prompt for parameters and create a stack
```

## RAG ingestion
```bash
# Upload local ./docs to S3 and trigger StartIngestionJob for your KB
export DOCS_BUCKET=your-bucket
export KB_ID=kb-xxxxxxxx
export KB_DS_ID=ds-xxxxxxxx
python rag/ingest.py ./docs
```

## Endpoints
- `POST /triage` – Calls Bedrock Converse with optional Guardrails
- `POST /kb/query` – Calls Bedrock Knowledge Bases RetrieveAndGenerate

## Notes
- For production, add an HTTP API JWT authorizer (Cognito) and attach WAF.
- Replace wildcard IAM resources with least-privilege ARNs once you know the exact model, KB and bucket ARNs.
```

---

## .gitignore
```
.venv/
__pycache__/
.aws-sam/
*.pyc
.DS_Store
```

