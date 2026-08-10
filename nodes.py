from uuid import uuid4

from .state import APIKeyRequestState


def validate_request(
    state: APIKeyRequestState,
) -> APIKeyRequestState:
    """
    Validate the incoming API key request.
    """

    print("Node: validate_request")

    user_id = state.get("user_id")
    application_name = state.get("application_name")
    environment = state.get("environment")
    permissions = state.get("requested_permissions", [])

    if not user_id:
        return {
            "request_valid": False,
            "validation_message": "User ID is required.",
            "status": "validation_failed",
        }

    if not application_name:
        return {
            "request_valid": False,
            "validation_message": "Application name is required.",
            "status": "validation_failed",
        }

    if environment not in {
        "development",
        "staging",
        "production",
    }:
        return {
            "request_valid": False,
            "validation_message": "Invalid environment.",
            "status": "validation_failed",
        }

    if not permissions:
        return {
            "request_valid": False,
            "validation_message": "At least one permission is required.",
            "status": "validation_failed",
        }

    return {
        "request_valid": True,
        "validation_message": "Request validated successfully.",
        "request_id": str(uuid4()),
        "status": "validated",
    }


def check_approval(
    state: APIKeyRequestState,
) -> APIKeyRequestState:
    """
    Determine whether the API key request requires approval.
    """

    print("Node: check_approval")

    environment = state.get("environment")

    # For this project, production API keys require approval.
    if environment == "production":
        return {
            "approval_required": True,
            "approval_status": "pending",
            "status": "waiting_for_approval",
        }

    return {
        "approval_required": False,
        "approval_status": "approved",
        "approval_message": "Approval not required.",
        "status": "approved",
    }


def generate_api_key(
    state: APIKeyRequestState,
) -> APIKeyRequestState:
    """
    Generate an API key after approval.
    """

    print("Node: generate_api_key")

    api_key = f"ak_{uuid4().hex}"

    return {
        "api_key": api_key,
        "status": "key_generated",
    }


def save_request(
    state: APIKeyRequestState,
) -> APIKeyRequestState:
    """
    Placeholder for saving the final request.

    Later this node will store the API key request
    and its final status in PostgreSQL.
    """

    print("Node: save_request")

    return {
        "status": "completed",
    }
