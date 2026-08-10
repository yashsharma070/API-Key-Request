from langgraph.graph import END, START, StateGraph

from .nodes import (
    check_approval,
    generate_api_key,
    save_request,
    validate_request,
)
from .state import APIKeyRequestState


def route_after_validation(
    state: APIKeyRequestState,
) -> str:
    """
    Decide whether the request passed validation.
    """

    if state.get("request_valid"):
        return "check_approval"

    return END


def route_after_approval_check(
    state: APIKeyRequestState,
) -> str:
    """
    Decide whether the request requires approval.
    """

    if state.get("approval_required"):
        return END

    return "generate_api_key"


def build_graph():
    """
    Build the API key request workflow.
    """

    graph = StateGraph(APIKeyRequestState)

    # -----------------------------
    # Nodes
    # -----------------------------

    graph.add_node(
        "validate_request",
        validate_request,
    )

    graph.add_node(
        "check_approval",
        check_approval,
    )

    graph.add_node(
        "generate_api_key",
        generate_api_key,
    )

    graph.add_node(
        "save_request",
        save_request,
    )

    # -----------------------------
    # Start
    # -----------------------------

    graph.add_edge(
        START,
        "validate_request",
    )

    # -----------------------------
    # Validation routing
    # -----------------------------

    graph.add_conditional_edges(
        "validate_request",
        route_after_validation,
    )

    # -----------------------------
    # Approval routing
    # -----------------------------

    graph.add_conditional_edges(
        "check_approval",
        route_after_approval_check,
    )

    # -----------------------------
    # Normal workflow
    # -----------------------------

    graph.add_edge(
        "generate_api_key",
        "save_request",
    )

    graph.add_edge(
        "save_request",
        END,
    )

    return graph


workflow = build_graph()
