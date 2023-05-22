import telegram
from telegram.ext import Application,CommandHandler
import dotenv
import os
from service import now,discount, products


def get_token():
    return os.getenv("TOKEN_TG")


async def start_callback(update, context):
    await update.message.reply_text("Приветствую тебя, дорогой друг, у тебя есть только одна команда - /now [cafe]")


async def now_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).capitalize()
        app = now.Now(content, os.getenv(content.upper()))
        await update.message.reply_text(f"{app.return_revenue()}")
    else:
        first = now.Now("Duo", os.getenv("DUO"))
        second = now.Now("June", os.getenv("JUNE"))
        await update.message.reply_text(f"{first.return_revenue()}\n{second.return_revenue()}")


async def yesterday_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).capitalize()
        app = now.Now(content, os.getenv(content.upper()), True)
        await update.message.reply_text(f"{app.return_revenue()}")
    else:
        first = now.Now("Duo", os.getenv("DUO"), True)
        second = now.Now("June", os.getenv("JUNE"), True)
        await update.message.reply_text(f"{first.return_revenue()}\n{second.return_revenue()}")

async def discount_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).capitalize()
        app = discount.Discount(content, os.getenv(content.upper()))
        await update.message.reply_text(f"{app.return_discount()}")
    else:
        first = discount.Discount("Duo", os.getenv("DUO"))
        second = discount.Discount("June", os.getenv("JUNE"))
        await update.message.reply_text(f"{first.return_discount()}\n{second.return_discount()}")


async def products_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).capitalize()
        app = products.Products(content, os.getenv(content.upper()))
        await update.message.reply_text(f"{app.return_products()}")
    else:
        first = products.Products("Duo", os.getenv("DUO"))
        second = products.Products("June", os.getenv("JUNE"))
        await update.message.reply_text(f"{first.return_products()}\n{second.return_products()}")
def main():
    dotenv.load_dotenv()
    application = Application.builder().token(get_token()).build()

    start_command = CommandHandler("start", start_callback)
    now_command = CommandHandler("now", now_callback)
    yesterday_command = CommandHandler("yesterday", yesterday_callback)
    discount_command = CommandHandler("discount", discount_callback)
    products_command = CommandHandler("products", products_callback)

    application.add_handler(start_command)
    application.add_handler(now_command)
    application.add_handler(yesterday_command)
    application.add_handler(discount_command)
    application.add_handler(products_command)

    application.run_polling()


if __name__ == '__main__':
    main()