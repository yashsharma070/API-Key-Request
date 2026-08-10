from typing import TypedDict


class APIAccessRequestState(TypedDict, total=False):
    request_id: str

    user_name: str
    department: str
    api_name: str
    use_case: str

    has_permission: bool

    approval_required: bool
    approval_status: str
    approved_by: str
    rejection_reason: str

    access_granted: bool
    status: str
    error: str
