from uuid import uuid4

from langgraph.types import interrupt


def create_request(state):

    print("Node: create_request")

    return {
        "request_id": str(uuid4()),
        "status": "created",
    }


def validate_request(state):

    print("Node: validate_request")

    if not state.get("user_name"):
        return {
            "status": "validation_failed",
            "error": "User name is required.",
        }

    if not state.get("department"):
        return {
            "status": "validation_failed",
            "error": "Department is required.",
        }

    if not state.get("api_name"):
        return {
            "status": "validation_failed",
            "error": "API name is required.",
        }

    if not state.get("use_case"):
        return {
            "status": "validation_failed",
            "error": "Use case is required.",
        }

    return {
        "status": "validated",
    }


def check_permission(state):

    print("Node: check_permission")

    # Temporary:
    # Assume the user does not have permission.
    has_permission = False

    if has_permission:
        return {
            "has_permission": True,
            "approval_required": False,
            "approval_status": "not_required",
            "status": "permission_granted",
        }

    return {
        "has_permission": False,
        "approval_required": True,
        "approval_status": "pending",
        "status": "approval_required",
    }


def request_approval(state):

    print("Node: request_approval")

    decision = interrupt("API access approval required.")

    print("Approval decision received:", decision)

    if decision["decision"] == "approved":
        return {
            "approval_status": "approved",
            "approved_by": "admin",
            "status": "approved",
        }

    return {
        "approval_status": "rejected",
        "rejection_reason": decision["reason"],
        "status": "rejected",
    }


def grant_access(state):

    print("Node: grant_access")

    return {
        "access_granted": True,
        "status": "access_granted",
    }


def reject_request(state):

    print("Node: reject_request")

    return {
        "access_granted": False,
        "status": "request_rejected",
    }
