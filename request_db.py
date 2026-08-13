import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")


def create_request_table():

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS api_access_requests (
                    request_id TEXT PRIMARY KEY,
                    thread_id TEXT NOT NULL,

                    user_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    api_name TEXT NOT NULL,
                    use_case TEXT NOT NULL,

                    approval_status TEXT NOT NULL,
                    status TEXT NOT NULL,

                    approved_by TEXT,
                    rejection_reason TEXT,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

        connection.commit()


def save_request(
    request_id,
    thread_id,
    user_name,
    department,
    api_name,
    use_case,
    approval_status,
    status,
):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api_access_requests (
                    request_id,
                    thread_id,
                    user_name,
                    department,
                    api_name,
                    use_case,
                    approval_status,
                    status
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    request_id,
                    thread_id,
                    user_name,
                    department,
                    api_name,
                    use_case,
                    approval_status,
                    status,
                ),
            )

        connection.commit()


def get_pending_requests():

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
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
                    created_at
                FROM api_access_requests
                WHERE approval_status = 'pending'
                ORDER BY created_at DESC
                """
            )

            return cursor.fetchall()


def update_request(
    request_id,
    approval_status,
    status,
    approved_by=None,
    rejection_reason=None,
):

    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE api_access_requests
                SET
                    approval_status = %s,
                    status = %s,
                    approved_by = %s,
                    rejection_reason = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE request_id = %s
                """,
                (
                    approval_status,
                    status,
                    approved_by,
                    rejection_reason,
                    request_id,
                ),
            )

        connection.commit()
