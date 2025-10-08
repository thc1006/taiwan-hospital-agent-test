#!/usr/bin/env bash
# Run the API locally and send a sample request

set -euo pipefail

# Start the FastAPI app in the background
uvicorn services.api.main:app --port 8000 --reload &
SERVER_PID=$!

echo "API started with PID $SERVER_PID. Waiting for startup..."
sleep 2

echo "Sending sample request to /run ..."
curl -s -X POST "http://localhost:8000/run" \
    -H "Content-Type: application/json" \
    -d '{"task": "Optimize ED bed allocation and schedule nurses", "params": {"hospital": "demo"}}'

echo "Shutting down API."
kill $SERVER_PID