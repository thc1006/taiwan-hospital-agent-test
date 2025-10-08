"""Stub tool implementations and registry.

In a real system these tools would perform network requests,
database queries, or other side effects. Here they simply return
descriptive dictionaries to illustrate how the agent might interact
with them.
"""

from typing import Any, Callable, Dict


def http_get(args: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate an HTTP GET request.

    Args:
        args: Dictionary containing task and params.
    Returns:
        A dictionary describing the result of the GET request.
    """
    return {
        "tool": "http_get",
        "args": args,
        "result": "Fetched data (stub)",
    }


def sql_query(args: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate a SQL query.

    Args:
        args: Dictionary containing task and params.
    Returns:
        A dictionary describing the result of the SQL query.
    """
    return {
        "tool": "sql_query",
        "args": args,
        "result": "Query executed (stub)",
    }


def ticket_create(args: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate creating a ticket or work order.

    Args:
        args: Dictionary containing task and params.
    Returns:
        A dictionary describing the creation of a ticket.
    """
    return {
        "tool": "ticket_create",
        "args": args,
        "result": "Ticket created (stub)",
    }


# Registry mapping tool names to callables
TOOL_REGISTRY: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "http_get": http_get,
    "sql_query": sql_query,
    "ticket_create": ticket_create,
}