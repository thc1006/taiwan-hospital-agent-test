"""FastAPI service exposing the agent via HTTP.

This lightweight API provides two endpoints:

- **GET /health** – health check returning a simple status.
- **POST /run** – accepts a task and parameters, invokes the agent and
  returns the plan and results.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

from packages.agent_core.agent_client import AgentCoreClient


app = FastAPI(title="Hospital Agent API")
agent = AgentCoreClient()


class TaskRequest(BaseModel):
    """Schema for the /run request body."""

    task: str
    params: Dict[str, Any] = {}


@app.get("/health")
def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/run")
def run_task(request: TaskRequest) -> Dict[str, Any]:
    """Run a task through the agent and return the result."""
    result = agent.run(request.task, request.params)
    return result