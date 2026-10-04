import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = "8945387807:AAHEMtxB01ZRlKuO0mYewViX26Km-GxtJqk"
WEBHOOK_URL = "https://gamestatannouncerbot.onrender.com"  # ← اینو عوض کن!

# ─────────── بازی /play ───────────
async def play(update, context):
    if not context.args:
        await update.message.reply_text("فرمت: /play نام بازی")
        return
    game = " ".join(context.args)
    announcer = update.effective_user

    cb = f"join:{game}:{announcer.id}"
    keyboard = [[InlineKeyboardButton(f" جوین شو ({game})", callback_data=cb)]]
    reply = InlineKeyboardMarkup(keyboard)

    sent = await update.message.reply_text(
        f"{announcer.first_name} الان داره {game} بازی میکنه!\n"
        "هرکی خواس بیاد، دکمه رو بزنه",
        reply_markup=reply
    )

    # پین کردن پیام دکمهدار
    try:
        await sent.pin()
    except Exception:
        await update.message.reply_text("بات دسترسی نداشت کار نکرد امیرو صدا کنین بیاد درستش کنه")

# ─────────── جوین (کلیک روی دکمه) ───────────
async def join(update, context):
    query = update.callback_query
    await query.answer()

    _, game, announcer_id = query.data.split(":", 2)
    joiner = query.from_user

    await query.message.reply_text(
        f"<a href=\"tg://user?id={announcer_id}\">بازیکن</a>! "
        f"{joiner.first_name} برای بازی {game} با تو آمادهست!",
        parse_mode="HTML"
    )

# ─────────── اجرای بات ───────────
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("play", play))
app.add_handler(CallbackQueryHandler(join))

if __name__ == "__main__":
    if os.environ.get("RENDER"):
        # ── روی Render: از webhook استفاده کن ──
        app.run_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path=TOKEN,
            webhook_url=WEBHOOK_URL + TOKEN
        )
    else:
        # ── توی کامپیوتر خودت: polling ──
        app.run_polling()
