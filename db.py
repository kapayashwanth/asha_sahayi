import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

# ---------- ASHA ----------
def get_or_create_asha(telegram_id):
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT * FROM asha_workers WHERE telegram_id=%s", (telegram_id,))
    user = cur.fetchone()

    if not user:
        cur.execute(
            "INSERT INTO asha_workers (telegram_id) VALUES (%s)",
            (telegram_id,)
        )
        db.commit()
        cur.execute("SELECT * FROM asha_workers WHERE telegram_id=%s", (telegram_id,))
        user = cur.fetchone()

    db.close()
    return user

def verify_asha(telegram_id, asha_id, phone):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE asha_workers
        SET asha_id=%s, phone=%s, verified=TRUE
        WHERE telegram_id=%s
    """, (asha_id, phone, telegram_id))
    db.commit()
    db.close()

def update_language(telegram_id, lang):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE asha_workers SET preferred_language=%s WHERE telegram_id=%s",
        (lang, telegram_id)
    )
    db.commit()
    db.close()

def is_verified(telegram_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT verified FROM asha_workers WHERE telegram_id=%s",
        (telegram_id,)
    )
    user = cur.fetchone()
    db.close()
    return user and user["verified"]

# ---------- VISITS ----------
def log_visit(asha_id, age, category, symptoms, action):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO patient_visits
        (asha_id, patient_age, category, symptoms, action_taken, referral_required)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (asha_id, age, category, symptoms, action, True))
    db.commit()
    db.close()

# ---------- ADMIN ----------
def get_all_asha():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT asha_id, phone, verified FROM asha_workers")
    rows = cur.fetchall()
    db.close()
    return rows

def get_recent_visits():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT v.category, v.patient_age, v.visit_date
        FROM patient_visits v
        ORDER BY v.visit_date DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    db.close()
    return rows

# ---------- AI LOG ----------
def log_ai_query(asha_id, query, response):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO ai_queries (asha_id, query_text, response_summary)
        VALUES (%s, %s, %s)
    """, (asha_id, query, response[:200]))
    db.commit()
    db.close()
