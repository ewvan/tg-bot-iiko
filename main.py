import telegram
from telegram.ext import Application,CommandHandler,Updater
import dotenv
import os
from service import revenue


def get_token():
    return os.getenv("TOKEN_TG")


async def start_callback(update, context):
    await update.message.reply_text("Приветствую тебя, дорогой друг, у тебя есть только одна команда - /revenue [cafe]")


async def revenue_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).capitalize()
        app = revenue.Revenue(content, os.getenv(content.upper()))
        await update.message.reply_text(f"{app.return_revenue()}")
    else:
        first = revenue.Revenue("Duo", os.getenv("DUO"))
        second = revenue.Revenue("June", os.getenv("JUNE"))
        await update.message.reply_text(f"{first.return_revenue()}\n{second.return_revenue()}")

def main():
    dotenv.load_dotenv()
    application = Application.builder().token(get_token()).build()

    start_command = CommandHandler("start", start_callback)
    revenue_command = CommandHandler("revenue", revenue_callback)
    application.add_handler(start_command)
    application.add_handler(revenue_command)
    application.run_polling()


if __name__ == '__main__':
    main()