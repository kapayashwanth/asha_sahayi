import os
import mysql.connector
from urllib.parse import urlparse


def get_db():
    """
    Creates and returns a MySQL connection using DATABASE_URL
    Works on Railway (private network) and locally.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("❌ DATABASE_URL environment variable not set")

    parsed = urlparse(database_url)

    return mysql.connector.connect(
        host=parsed.hostname,
        port=parsed.port or 3306,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path.lstrip("/"),
        autocommit=True
    )


# ---------------- ASHA WORKER ----------------
def is_verified(telegram_id):
    """
    Returns True if ASHA worker is verified, else False
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT verified FROM asha_workers WHERE telegram_id = %s",
        (telegram_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    db.close()

    if row:
        return bool(row["verified"])
    return False


def get_or_create_asha(telegram_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM asha_workers WHERE telegram_id = %s",
        (telegram_id,)
    )
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            """
            INSERT INTO asha_workers (telegram_id)
            VALUES (%s)
            """,
            (telegram_id,)
        )

        cursor.execute(
            "SELECT * FROM asha_workers WHERE telegram_id = %s",
            (telegram_id,)
        )
        user = cursor.fetchone()

    cursor.close()
    db.close()
    return user


def update_language(telegram_id, language):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE asha_workers
        SET preferred_language = %s
        WHERE telegram_id = %s
        """,
        (language, telegram_id)
    )

    cursor.close()
    db.close()


def verify_asha(telegram_id, asha_id, phone):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE asha_workers
        SET asha_id = %s,
            phone = %s,
            verified = TRUE
        WHERE telegram_id = %s
        """,
        (asha_id, phone, telegram_id)
    )

    cursor.close()
    db.close()


# ---------------- PATIENT VISITS ----------------

def log_patient_visit(asha_db_id, age, category, symptoms, action, referral):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO patient_visits
        (asha_id, patient_age, category, symptoms, action_taken, referral_required)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (asha_db_id, age, category, symptoms, action, referral)
    )

    cursor.close()
    db.close()


# ---------------- AI QUERIES ----------------

def log_ai_query(asha_db_id, query_text, response_summary):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO ai_queries (asha_id, query_text, response_summary)
        VALUES (%s, %s, %s)
        """,
        (asha_db_id, query_text, response_summary)
    )

    cursor.close()
    db.close()

