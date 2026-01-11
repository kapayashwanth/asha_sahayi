import os
from dotenv import load_dotenv
from google.genai import Client

from db import get_or_create_asha, log_ai_query

load_dotenv()

client = Client(api_key=os.getenv("AI_API_KEY"))

SYSTEM_PROMPT = """
You are ASHA Sahayi, assisting ASHA workers in India.

STRICT RULES:
- Maximum 5 bullet points or 5 short lines only
- Very simple language
- No diagnosis
- No medicines
- Focus on what ASHA worker should observe and do
- Always mention referral to PHC if symptoms are serious
"""


def get_ai_response(query, telegram_id):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=SYSTEM_PROMPT + "\n" + query
    ).text

    asha = get_or_create_asha(telegram_id)
    log_ai_query(asha["id"], query, response)

    return response
