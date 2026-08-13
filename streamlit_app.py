import uuid

import streamlit as st
from database import get_checkpointer
from graph import workflow
from langgraph.types import Command
from request_db import (
    get_pending_requests,
    save_request,
    update_request,
)

st.set_page_config(
    page_title="API Access Request",
    page_icon="🔑",
)


# =================================================
# USER REQUEST
# =================================================


def user_request_page():

    st.title("API key request")

    with st.form("api_access_request"):
        user_name = st.text_input(
            "Name",
            placeholder="Enter your name",
        )

        department = st.selectbox(
            "Department",
            [
                "Engineering",
                "Data Science",
                "Product",
                "Marketing",
                "Finance",
                "HR",
            ],
        )

        api_name = st.selectbox(
            "API",
            [
                "OpenAI API",
                "Google Gemini API",
                "AWS API",
                "GitHub API",
            ],
        )

        use_case = st.text_area("Reason")

        submitted = st.form_submit_button("Request Access")

    if submitted:
        if not user_name.strip():
            st.error("Please enter your name.")
            return

        if not use_case.strip():
            st.error("Please provide a reason or use case.")
            return

        with st.spinner("Submitting request..."):
            # Create request ID
            request_id = str(uuid.uuid4())

            thread_id = request_id

            # Initial request state
            request = {
                "request_id": request_id,
                "user_name": user_name.strip(),
                "department": department,
                "api_name": api_name,
                "use_case": use_case.strip(),
                "status": "pending",
            }

            # Start Langgraph
            with get_checkpointer() as checkpointer:
                app = workflow.compile(checkpointer=checkpointer)

                result = app.invoke(
                    request,
                    config={"configurable": {"thread_id": thread_id}},
                )

            # Save the request

            save_request(
                request_id=request_id,
                thread_id=thread_id,
                user_name=user_name.strip(),
                department=department,
                api_name=api_name,
                use_case=use_case.strip(),
                approval_status=result.get(
                    "approval_status",
                    "pending",
                ),
                status=result.get(
                    "status",
                    "pending",
                ),
            )

        st.success("Your API access request has been submitted.")

        st.info(f"Request ID: {request_id}")

        if "__interrupt__" in result:
            st.warning("Your request is waiting for admin approval.")

        else:
            st.success("Your API access request has been completed.")


# admin panel
def admin_page():

    st.title("Admin")

    pending_requests = get_pending_requests()

    if not pending_requests:
        st.success("There are no pending API access requests.")

        return

    st.write(f"Pending requests: {len(pending_requests)}")

    for request in pending_requests:
        (
            request_id,
            thread_id,
            user_name,
            department,
            api_name,
            use_case,
            approval_status,
            status,
            approved_by,
            rejection_reason,
            created_at,
        ) = request

        with st.container(border=True):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**User:** {user_name}")

                st.write(f"**Department:** {department}")

                st.write(f"**API:** {api_name}")

            with col2:
                st.write(f"**Status:** {approval_status}")

                st.write(f"**Created:** {created_at}")

            st.write(f"**Reason:** {use_case}")

            # Admin action buttons
            approve_col, reject_col = st.columns(2)

            with approve_col:
                approve_clicked = st.button(
                    "Approve",
                    key=f"approve_{request_id}",
                )

            with reject_col:
                reject_clicked = st.button(
                    "Reject",
                    key=f"reject_{request_id}",
                )

            # Approve
            if approve_clicked:
                with st.spinner("Approving request..."):
                    with get_checkpointer() as checkpointer:
                        app = workflow.compile(checkpointer=checkpointer)

                        result = app.invoke(
                            Command(resume={"decision": "approved"}),
                            config={"configurable": {"thread_id": thread_id}},
                        )

                    update_request(
                        request_id=request_id,
                        approval_status="approved",
                        status=result.get(
                            "status",
                            "access_granted",
                        ),
                        approved_by="admin",
                    )

                st.success("API access approved successfully.")

                st.rerun()

            # Reject
            if reject_clicked:
                st.session_state[f"rejecting_{request_id}"] = True

                st.rerun()

            # Rejection form
            if st.session_state.get(
                f"rejecting_{request_id}",
                False,
            ):
                reason = st.text_input(
                    "Rejection reason",
                    key=f"reason_{request_id}",
                )

                confirm_rejection = st.button(
                    "Confirm Rejection",
                    key=f"confirm_reject_{request_id}",
                )

                if confirm_rejection:
                    if not reason.strip():
                        st.error("Please provide a rejection reason.")

                    else:
                        with st.spinner("Rejecting request..."):
                            with get_checkpointer() as checkpointer:
                                app = workflow.compile(checkpointer=checkpointer)

                                result = app.invoke(
                                    Command(
                                        resume={
                                            "decision": "rejected",
                                            "reason": reason.strip(),
                                        }
                                    ),
                                    config={"configurable": {"thread_id": thread_id}},
                                )

                            update_request(
                                request_id=request_id,
                                approval_status="rejected",
                                status=result.get(
                                    "status",
                                    "request_rejected",
                                ),
                                rejection_reason=reason.strip(),
                            )

                        st.error("API access request rejected.")

                        st.rerun()


user_tab, admin_tab = st.tabs(
    [
        "Key request",
        "Admin",
    ]
)


with user_tab:
    user_request_page()


with admin_tab:
    admin_page()
