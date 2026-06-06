from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
    ContextTypes,
    filters,
)
import os

PASSWORD = "blaue Blume"
CHANNEL_ID = -1003872961450

pending_users = set()
authenticated_users = set()


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user

    pending_users.add(user.id)

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text="Willkommen! Bitte gib das Passwort ein, um Zugang zum Kanal zu erhalten."
        )
    except Exception as e:
        print(e)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bitte gib das Passwort ein."
    )


async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in pending_users:
        return

    if text == PASSWORD:
        try:
            await context.bot.approve_chat_join_request(
                chat_id=CHANNEL_ID,
                user_id=user_id
            )

            authenticated_users.add(user_id)
            pending_users.remove(user_id)

            await update.message.reply_text(
                "Passwort korrekt. Deine Beitrittsanfrage wurde genehmigt."
            )

        except Exception as e:
            await update.message.reply_text(
                f"Fehler: {e}"
            )

    else:
        await update.message.reply_text(
            "Falsches Passwort. Bitte versuche es erneut."
        )


def main():
    app = Application.builder().token(os.environ.get("TELEGRAM_TOKEN")).build()


    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(join_request))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

    app.run_polling()


if __name__ == "__main__":
    main()
