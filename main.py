import asyncio
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
    content = context.args[-1].strip()
    app = revenue.Revenue(content)
    await update.message.reply_text(f"{app.return_revenue()}")



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