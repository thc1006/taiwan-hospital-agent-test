#!/usr/bin/env bash
# Set up Python environment and install dependencies

set -euo pipefail

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

source .venv/bin/activate
pip install -U pip
# Install core dependencies
pip install fastapi uvicorn boto3 pydantic pytest graphviz

echo "Development environment bootstrapped. Activate with 'source .venv/bin/activate'."