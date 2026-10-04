import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = "8945387807:AAHEMtxB01ZRlKuO0mYewViX26Km-GxtJqk"
WEBHOOK_URL = "https://gamestatannouncerbot.onrender.com/"

# ---------- بازی /play ----------
async def play(update, context):
    if not context.args:
        await update.message.reply_text("فرمت: /play نام بازی")
        return

    game = " ".join(context.args)
    announcer = update.effective_user

    cb = f"join:{game}:{announcer.id}"
    keyboard = [[InlineKeyboardButton(f" جوین شو ({game})", callback_data=cb)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent = await update.message.reply_text(
        f"{announcer.first_name} الان داره {game} بازی میکنه!\n"
        "هرکی خواس بیاد، دکمه رو بزنه",
        reply_markup=reply_markup
    )

    # ذخیرهی پیام و چت برای پایان بازی
    context.bot_data["active_game"] = {
        "chat_id": update.effective_chat.id,
        "message_id": sent.message_id
    }

    # پین کردن پیام دکمهدار
    try:
        await sent.pin()
    except Exception:
        await update.message.reply_text("بات دسترسی نداشت کار نکرد امیرو صدا کنین بیاد درستش کنه")

# ---------- پایان بازی /end ----------
async def end(update, context):
    active = context.bot_data.get("active_game")

    if active:
        try:
            await context.bot.unpin_chat_message(
                chat_id=active["chat_id"],
                message_id=active["message_id"]
            )
        except Exception:
            pass
        context.bot_data["active_game"] = None

    await update.message.reply_text(
        f"🏁 {update.effective_user.first_name} اعلام کرد که دیگه بازی نمیکنه!"
    )

# ---------- جوین (کلیک روی دکمه) ----------
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

# ---------- اجرای بات ----------
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("play", play))
app.add_handler(CommandHandler("end", end))
app.add_handler(CallbackQueryHandler(join))

if __name__ == "__main__":
    if os.environ.get("RENDER"):
        app.run_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path=TOKEN,
            webhook_url=WEBHOOK_URL + TOKEN
        )
    else:
        app.run_polling()
