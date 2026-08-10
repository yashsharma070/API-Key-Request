from langgraph.types import Command

from .database import get_checkpointer
from .graph import workflow


def main():

    request = {
        "user_name": "Yash",
        "department": "Engineering",
        "api_name": "OpenAI API",
        "use_case": "Build an internal AI assistant",
        "status": "pending",
    }

    config = {"configurable": {"thread_id": "api-request-001"}}

    print("\nStarting API access request...\n")

    with get_checkpointer() as checkpointer:
        app = workflow.compile(checkpointer=checkpointer)

        # -----------------------------
        # Start workflow
        # -----------------------------

        result = app.invoke(
            request,
            config=config,
        )

        # -----------------------------
        # Check for interrupt
        # -----------------------------

        if "__interrupt__" in result:
            print("\nWorkflow interrupted.")
            print("Waiting for admin approval.\n")

            print("Request details:")
            print(f"User: {request['user_name']}")
            print(f"Department: {request['department']}")
            print(f"API: {request['api_name']}")
            print(f"Use case: {request['use_case']}")

            # -----------------------------
            # Admin decision
            # -----------------------------

            decision = input("\nAdmin decision (approve/reject): ").strip().lower()

            if decision == "approve":
                approval = {"decision": "approved"}

            elif decision == "reject":
                reason = input("Rejection reason: ").strip()

                approval = {
                    "decision": "rejected",
                    "reason": reason,
                }

            else:
                print("\nInvalid decision. Please enter approve or reject.")

                return

            # -----------------------------
            # Resume workflow
            # -----------------------------

            result = app.invoke(
                Command(resume=approval),
                config=config,
            )

        # -----------------------------
        # Final result
        # -----------------------------

        print("\nWorkflow completed.")

        print("\nFinal state:")
        print(result)

        # -----------------------------
        # User-friendly result
        # -----------------------------

        if result.get("access_granted"):
            print("\n✅ API access granted.")

        elif result.get("approval_status") == "rejected":
            print("\n❌ API access rejected.")

            print(
                "Reason:",
                result.get("rejection_reason"),
            )


if __name__ == "__main__":
    main()
