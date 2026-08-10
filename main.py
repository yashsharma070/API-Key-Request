from .database import get_checkpointer
from .graph import workflow


def main():

    request = {
        "user_id": "user-123",
        "application_name": "payment-service",
        "environment": "development",
        "requested_permissions": [
            "read",
            "write",
        ],
        "status": "received",
    }

    config = {"configurable": {"thread_id": "api-request-001"}}

    print("\nStarting API key request...\n")

    with get_checkpointer() as checkpointer:
        app = workflow.compile(checkpointer=checkpointer)

        result = app.invoke(
            request,
            config=config,
        )

    print("\nWorkflow completed.")

    print("\nFinal state:")

    print(result)


if __name__ == "__main__":
    main()
