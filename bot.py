from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
import os
from dotenv import load_dotenv

from texts import LANG, PREGNANCY_GUIDE, CHILD_GUIDE, NUTRITION_GUIDE
from db import (
    get_or_create_asha, verify_asha, update_language,
    is_verified, log_visit, get_all_asha, get_recent_visits
)
from ai import get_ai_response

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_IDS = [1472652264]  # ← replace

user_lang = {}
user_state = {}
visit_form = {}
auth_form = {}

# ---------- MENU ----------
async def main_menu(update, context):
    uid = update.effective_user.id
    lang = user_lang.get(uid, "en")

    keyboard = [
        [InlineKeyboardButton("🌐 Language", callback_data="lang")],
        [InlineKeyboardButton("🩺 Medical Guidance", callback_data="guide")],
        [InlineKeyboardButton("📝 Log Visit", callback_data="log")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]

    if uid in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton("🛠 Admin Dashboard", callback_data="admin")])

    text = f"{LANG[lang]['welcome']}\n\n{LANG[lang]['menu']}"

    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ---------- START ----------
async def start(update, context):
    uid = update.effective_user.id
    user = get_or_create_asha(uid)

    if not user["verified"]:
        user_state[uid] = "AUTH_ID"
        await update.message.reply_text("🔐 Enter ASHA Worker ID:")
        return

    user_lang[uid] = user["preferred_language"]
    await main_menu(update, context)

# ---------- TEXT HANDLER ----------
async def text_handler(update, context):
    uid = update.effective_user.id
    text = update.message.text

    # AUTH
    if user_state.get(uid) == "AUTH_ID":
        auth_form[uid] = {"asha_id": text}
        user_state[uid] = "AUTH_PHONE"
        await update.message.reply_text("Enter registered mobile number:")
        return

    if user_state.get(uid) == "AUTH_PHONE":
        verify_asha(uid, auth_form[uid]["asha_id"], text)
        user_state[uid] = None
        auth_form[uid] = {}
        await update.message.reply_text("✅ Verification successful.")
        await start(update, context)
        return

    # AI QUESTION
    if user_state.get(uid) == "AI":
        user_state[uid] = None
        reply = get_ai_response(text, uid)
        await update.message.reply_text(reply + "\n\n⚠️ Refer to PHC if needed.")
        await main_menu(update, context)
        return

    # VISIT FORM
    if user_state.get(uid) == "VISIT_AGE":
        if not text.isdigit():
            await update.message.reply_text("Enter valid age:")
            return
        visit_form[uid]["age"] = int(text)
        user_state[uid] = "VISIT_SYM"
        await update.message.reply_text("Enter symptoms:")
        return

    if user_state.get(uid) == "VISIT_SYM":
        asha = get_or_create_asha(uid)
        log_visit(
            asha["id"],
            visit_form[uid]["age"],
            "General",
            text,
            "Recorded by ASHA"
        )
        user_state[uid] = None
        visit_form[uid] = {}
        await update.message.reply_text("✅ Visit logged.")
        await main_menu(update, context)

# ---------- ROUTER ----------
async def router(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    if q.data == "lang":
        await q.edit_message_text(
            "Select Language:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("English", callback_data="set_en")],
                [InlineKeyboardButton("हिंदी", callback_data="set_hi")],
                [InlineKeyboardButton("தமிழ்", callback_data="set_ta")],
                [InlineKeyboardButton("മലയാളം", callback_data="set_ml")]
            ])
        )

    elif q.data.startswith("set_"):
        code = q.data.split("_")[1]
        user_lang[uid] = code
        update_language(uid, code)
        await q.edit_message_text(LANG[code]["lang_set"])
        await main_menu(update, context)

    elif q.data == "guide":
        await q.edit_message_text(
            "Choose:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤰 Pregnancy", callback_data="gp")],
                [InlineKeyboardButton("👶 Child", callback_data="gc")],
                [InlineKeyboardButton("🥗 Nutrition", callback_data="gn")],
                [InlineKeyboardButton("🤖 Ask AI", callback_data="ai")]
            ])
        )

    elif q.data == "gp":
        await q.edit_message_text(PREGNANCY_GUIDE, parse_mode="Markdown")

    elif q.data == "gc":
        await q.edit_message_text(CHILD_GUIDE, parse_mode="Markdown")

    elif q.data == "gn":
        await q.edit_message_text(NUTRITION_GUIDE, parse_mode="Markdown")

    elif q.data == "ai":
        user_state[uid] = "AI"
        await q.edit_message_text("🤖 Type your health question:")

    elif q.data == "log":
        visit_form[uid] = {}
        user_state[uid] = "VISIT_AGE"
        await q.edit_message_text("📝 Enter patient age:")

    elif q.data == "admin":
        workers = get_all_asha()
        text = "👥 ASHA Workers:\n"
        for w in workers:
            text += f"{w['asha_id']} | {w['phone']} | Verified: {w['verified']}\n"
        await q.edit_message_text(text)

    elif q.data == "help":
        await q.edit_message_text("ASHA Sahayi provides safe guidance.\nNo diagnosis.")

# ---------- APP ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(router))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

print("🤖 ASHA Sahayi is running...")
app.run_polling()
