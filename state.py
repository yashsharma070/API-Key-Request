from typing import Literal

from typing_extensions import TypedDict


class APIKeyRequestState(TypedDict, total=False):
    # -------------------------
    # Request information
    # -------------------------
    user_id: str
    application_name: str
    environment: Literal["development", "staging", "production"]
    requested_permissions: list[str]

    # -------------------------
    # Validation
    # -------------------------
    request_valid: bool
    validation_message: str

    # -------------------------
    # Approval
    # -------------------------
    approval_required: bool
    approval_status: Literal["pending", "approved", "rejected"]
    approved_by: str
    approval_message: str

    # -------------------------
    # API key
    # -------------------------
    api_key: str | None

    # -------------------------
    # Workflow information
    # -------------------------
    request_id: str
    status: str
