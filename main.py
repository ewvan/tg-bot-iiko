import telegram
from telegram.constants import ParseMode
from telegram.ext import Application,CommandHandler
import dotenv
import os
from service import now,discount, products, lfl
from get_parameters import get_parameters

def get_token():
    return os.getenv("TOKEN_TG")

async def start_callback(update, context):
    await update.message.reply_text("Приветствую тебя, дорогой друг, у тебя есть такие команды, как /now [cafe], /yesterday [cafe], /products [cafe], /discount [cafe]")


async def now_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).upper()
        cafe_parameters = get_parameters(content)
        app = now.Now(cafe_parameters["name"], cafe_parameters["link"])
        await update.message.reply_text(f"{app.return_revenue()}",parse_mode=ParseMode.HTML)
    else:
        cafe_parameters = get_parameters()
        result = ""
        for cafe, data in cafe_parameters.items():
            app = now.Now(data["name"],data["link"])
            result += app.return_revenue() + '\n'
            del app
        await update.message.reply_text(result,parse_mode=ParseMode.HTML)


async def yesterday_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).upper()
        cafe_parameters = get_parameters(content)
        app = now.Now(cafe_parameters["name"], cafe_parameters["link"], True)
        await update.message.reply_text(f"{app.return_revenue()}", parse_mode=ParseMode.HTML)
    else:
        cafe_parameters = get_parameters()
        result = ""
        for cafe, data in cafe_parameters.items():
            app = now.Now(data["name"], data["link"], True)
            result += app.return_revenue() + '\n'
            del app
        await update.message.reply_text(result, parse_mode=ParseMode.HTML)

async def discount_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).upper()
        cafe_parameters = get_parameters(content)
        app = discount.Discount(cafe_parameters["name"], cafe_parameters["link"])
        await update.message.reply_text(f"{app.return_discount()}", parse_mode=ParseMode.HTML)
    else:
        cafe_parameters = get_parameters()
        result = ""
        for cafe, data in cafe_parameters.items():
            app = discount.Discount(data["name"], data["link"])
            result += app.return_discount() + '\n'
            del app
        await update.message.reply_text(result, parse_mode=ParseMode.HTML)


async def lfl_callback(update, context):
    if len(context.args) > 0:
        content = (context.args[-1].strip()).upper()
        cafe_parameters = get_parameters(content)
        app = lfl.Lfl(cafe_parameters["name"], cafe_parameters["link"])
        await update.message.reply_text(f"{app.return_revenue()}", parse_mode=ParseMode.HTML)
    else:
        cafe_parameters = get_parameters()
        result = ""
        for cafe, data in cafe_parameters.items():
            app = lfl.Lfl(data["name"], data["link"])
            result += app.return_revenue() + '\n'
            del app
        await update.message.reply_text(result, parse_mode=ParseMode.HTML)

async def products_callback(update, context):

    if len(context.args) > 0:
        content = (context.args[-1].strip()).upper()
        cafe_parameters = get_parameters(content)
        app = products.Products(cafe_parameters["name"], cafe_parameters["link"])
        await update.message.reply_text(f"{app.return_products()}", parse_mode=ParseMode.HTML)
    else:
        cafe_parameters = get_parameters()
        result = ""
        for cafe, data in cafe_parameters.items():
            app = products.Products(data["name"], data["link"])
            result += app.return_products() + '\n'
            del app
        await update.message.reply_text(result, parse_mode=ParseMode.HTML)

def main():
    dotenv.load_dotenv()
    application = Application.builder().token(get_token()).build()

    start_command = CommandHandler("start", start_callback)
    now_command = CommandHandler("now", now_callback)
    yesterday_command = CommandHandler("yesterday", yesterday_callback)
    discount_command = CommandHandler("discount", discount_callback)
    products_command = CommandHandler("products", products_callback)
    lfl_command = CommandHandler("lfl", lfl_callback)

    application.add_handler(start_command)
    application.add_handler(now_command)
    application.add_handler(yesterday_command)
    application.add_handler(discount_command)
    application.add_handler(products_command)
    application.add_handler(lfl_command)

    application.run_polling()


if __name__ == '__main__':
    main()