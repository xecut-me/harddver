from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from secret import SECRET_TELEGRAM_API_KEY
from selenium import webdriver
from telegram import Update
import signal
import json
import sys
import os


admin_chat_id = -1002571293789
no_auth_msg = "Это админская команда, работает только в чате https://t.me/+IBkZEqKkqRlhNGQy"
DEFAULT_URL = "https://xecut-me.github.io/harddver/"

os.environ['DISPLAY'] = ':0'

options = Options()
options.add_argument("--kiosk")
options.add_argument("--no-first-run")
options.add_argument("--disable-infobars")
options.add_argument("--noerrdialogs")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
driver.get(DEFAULT_URL)


def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id != admin_chat_id:
            await update.message.reply_text(no_auth_msg)
            return
        await func(update, context)
    return wrapper


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        json.dumps(update.to_dict(), ensure_ascii=False, indent=2)
    )


@admin_only
async def reload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOT IMPLEMENTED 🔄 Страница обновлена")


@admin_only
async def produrl_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOT IMPLEMENTED 🌐 Продовый URL: https://example.com")


@admin_only
async def url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Укажите URL после команды.")
        return
    custom_url = context.args[0]
    await update.message.reply_text(f"NOT IMPLEMENTED ✅ Кастомный URL установлен: {custom_url}")


@admin_only
async def deploy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("NOT IMPLEMENTED 🚀 Бот деплоится...")


def cleanup(signum, frame):
    driver.quit()
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


application: Application = Application.builder().token(SECRET_TELEGRAM_API_KEY).build()

application.add_handler(CommandHandler("reload", reload_handler))
application.add_handler(CommandHandler("produrl", produrl_handler))
application.add_handler(CommandHandler("url", url_handler))
application.add_handler(CommandHandler("deploy", deploy_handler))
application.add_handler(MessageHandler(filters.ALL, message_handler))

application.run_polling()
