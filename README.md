# Hospital Agent MVP

This repository contains a proof‑of‑concept AI agent built for the **AWS AI Agent Global Hackathon**.  
The agent demonstrates how Amazon Bedrock AgentCore can orchestrate tools and services to alleviate emergency department (ED) congestion and nursing scheduling challenges in Taiwan.

## Features

* Uses **Amazon Bedrock AgentCore** (or Nova / SageMaker) to reason about tasks and route tool calls.
* Implements a simple tool registry (`http_get`, `sql_query`, `ticket_create`) to interact with external services.
* Provides a **FastAPI** service with endpoints `/run` and `/health`.
* Includes **Infrastructure as Code** (Terraform) to deploy the API behind API Gateway and Lambda with necessary IAM roles.
* Supplies scripts to bootstrap development, run locally, and render the system architecture diagram.
* Contains a research report summarising the pain points in Taiwan’s hospital triage and manpower system (see `RESEARCH.md`).

## Getting Started

### Prerequisites

- Python 3.10+
- AWS CLI configured with access to Bedrock and other services
- Terraform

### Local Development

```sh
make bootstrap     # set up Python environment, install dependencies
make dev           # run API locally via uvicorn
make demo          # send a sample request to /run
```

### Deployment to AWS

See `infra/main.tf` for Terraform configuration. Populate the variables for your AWS account and run:

```sh
cd infra
terraform init
terraform apply
```

This will create an API Gateway, Lambda function, S3 bucket, and IAM roles. For production use you should secure secrets and fine‑tune IAM policies.

## Project Structure

```
hospital_agent_mvp/
├── RESEARCH.md    # research on ED congestion and nursing shortage
├── README.md      # overview and setup instructions
├── SUBMISSION.md  # template for hackathon submission
├── packages/
│   └── agent_core/
│       ├── __init__.py
│       ├── agent_client.py  # stub client for Bedrock AgentCore
│       └── tools.py         # stub tool registry
├── services/
│   └── api/
│       └── main.py          # FastAPI app
├── infra/
│   └── main.tf              # Terraform resources
├── scripts/
│   ├── dev_bootstrap.sh     # install dependencies and linters
│   ├── local_demo.sh        # run a local demo
│   └── render_arch.py       # generate architecture diagram
├── docs/
│   └── arch.png             # architecture diagram (generated)
├── Makefile
└── LICENSE
```

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.