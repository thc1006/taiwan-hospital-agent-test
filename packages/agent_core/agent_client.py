"""Simple stub client for Amazon Bedrock AgentCore.

This client demonstrates how a high‑level orchestration layer might
interact with AgentCore. In a production implementation you would
authenticate with Bedrock, send your prompt and current context to
AgentCore, receive a plan and tool calls back, execute them, and
return the final response.
"""

from typing import Any, Dict, List
from .tools import TOOL_REGISTRY


class AgentCoreClient:
    """Stub agent client that simulates planning and tool execution."""

    def __init__(self, model_id: str = "bedrock-model") -> None:
        self.model_id = model_id

    def run(self, task: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using a simple hard‑coded plan.

        Args:
            task: The natural language description of the task.
            params: Additional parameters for the task.

        Returns:
            A dictionary containing the plan, intermediate results and a stub report.
        """
        # In a real implementation you would call AgentCore here to produce a plan.
        plan: List[str] = ["http_get", "sql_query", "ticket_create"]
        results = []
        for tool_name in plan:
            tool = TOOL_REGISTRY.get(tool_name)
            if tool:
                # Each tool receives the same args in this stub
                result = tool({"task": task, "params": params})
                results.append(result)
        report = (
            f"Executed plan {plan} for task '{task}'. "
            "This is a stub report summarising the actions taken."
        )
        return {
            "task": task,
            "plan": plan,
            "results": results,
            "report": report,
        }