from langgraph.graph import END, START, StateGraph

from .nodes import (
    check_permission,
    create_request,
    grant_access,
    reject_request,
    request_approval,
    validate_request,
)
from .state import APIAccessRequestState


def route_after_validation(state):

    if state.get("status") == "validated":
        return "check_permission"

    return END


def route_after_permission_check(state):

    if state.get("has_permission"):
        return "grant_access"

    return "request_approval"


def route_after_approval(state):

    if state.get("approval_status") == "approved":
        return "grant_access"

    return "reject_request"


def build_graph():

    graph = StateGraph(APIAccessRequestState)

    # -----------------------------
    # Add nodes
    # -----------------------------

    graph.add_node(
        "create_request",
        create_request,
    )

    graph.add_node(
        "validate_request",
        validate_request,
    )

    graph.add_node(
        "check_permission",
        check_permission,
    )

    graph.add_node(
        "request_approval",
        request_approval,
    )

    graph.add_node(
        "grant_access",
        grant_access,
    )

    graph.add_node(
        "reject_request",
        reject_request,
    )

    # -----------------------------
    # Start
    # -----------------------------

    graph.add_edge(
        START,
        "create_request",
    )

    graph.add_edge(
        "create_request",
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
    # Permission routing
    # -----------------------------

    graph.add_conditional_edges(
        "check_permission",
        route_after_permission_check,
    )

    # -----------------------------
    # Approval routing
    # -----------------------------

    graph.add_conditional_edges(
        "request_approval",
        route_after_approval,
    )

    # -----------------------------
    # Final nodes
    # -----------------------------

    graph.add_edge(
        "grant_access",
        END,
    )

    graph.add_edge(
        "reject_request",
        END,
    )

    return graph


workflow = build_graph()
