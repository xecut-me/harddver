from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import MessageEntityType
from secret import SECRET_TELEGRAM_API_KEY
from dverchrome import DEFAULT_URL
from telegram import Update
from io import BytesIO
from PIL import Image
from time import time
from mss import mss
import subprocess
import json
import sys


admin_chat_id = -1002571293789
admin_not_allowed = "Это админская команда, работает только в чате https://t.me/+IBkZEqKkqRlhNGQy"

xecut_chat_id = -1002089160630
xecut_not_allowed = "Эта команда работает в чате хакспейса Xecut https://t.me/xecut_chat"


def allowed_chats_only(allowed_chat_ids, not_allowed_message):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message.forward_from or update.message.forward_from_chat:
                return
            
            if update.effective_chat.id not in allowed_chat_ids:
                await update.message.reply_text(not_allowed_message)
                return

            await func(update, context)
        return wrapper
    return decorator


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != xecut_chat_id:
        err_message = "Чтобы вывести сообщение на харддверь тегни меня в https://t.me/xecut_chat"
        await update.message.reply_text(err_message, disable_web_page_preview=True)
        return
    
    message = update.message
    bot_id = context.bot.id

    if not message:
        return

    is_mentioned = any(
        entity.type == MessageEntityType.MENTION and 
        message.text[entity.offset:entity.offset + entity.length].lower() == f"@{context.bot.username.lower()}"
        for entity in (message.entities or [])
    )

    is_reply_to_bot = (
        message.reply_to_message 
        and message.reply_to_message.from_user 
        and message.reply_to_message.from_user.id == bot_id
    )

    if not is_mentioned and not is_reply_to_bot:
        return

    update_json = json.dumps(update.to_dict(), ensure_ascii=False)
    response = driver.execute_script("return onMessage(arguments[0]);", update_json)
    
    if response:
        await update.message.reply_text(response, disable_web_page_preview=True)


@allowed_chats_only((admin_chat_id,), admin_not_allowed)
async def reload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    driver.refresh()
    await update.message.reply_text("🔄 Страница перезагружена " + state, disable_web_page_preview=True)


@allowed_chats_only((admin_chat_id,), admin_not_allowed)
async def url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and not context.args[0].startswith("http"):
        await update.message.reply_text("❌ URL должен начинаться с http")
        return
    
    if context.args:
        url = context.args[0]
        state = f"🌐🧪 Загружен тестовый URL {url}"
    else:
        url = DEFAULT_URL
        state = f"🌐🔒 Загружен продовый URL {url}"
    
    driver.get(url)
    await update.message.reply_text(state, disable_web_page_preview=True)


@allowed_chats_only((admin_chat_id,), admin_not_allowed)
async def deploy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subprocess.run(["git", "pull"])
    await update.message.reply_text("🚀 git pull = ok")

    driver.quit()
    await update.message.reply_text("🚀 driver.quit() = ok, крешимся для перезапуска супервизором 😂")
    
    sys.exit(0)


@allowed_chats_only((admin_chat_id, xecut_chat_id), xecut_not_allowed)
async def screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with mss() as sct:
        screenshot = sct.grab(sct.monitors[0])

    img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
    buffer = BytesIO()
    buffer.name = f"screenshot.png{time()}"
    img.save(buffer, format="PNG")
    buffer.seek(0)

    await update.message.reply_photo(photo=buffer)


async def init(app: Application) -> None:
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    commit_hash = result.stdout.strip()

    text = f"🎉 Я запустился! Версия https://github.com/xecut-me/harddver/tree/{commit_hash}"
    await app.bot.send_message(chat_id=admin_chat_id, text=text, disable_web_page_preview=True)


def start_bot(_driver):
    global driver
    driver = _driver

    application: Application = Application.builder().token(SECRET_TELEGRAM_API_KEY).post_init(init).build()

    application.add_handler(CommandHandler("reload", reload_handler))
    application.add_handler(CommandHandler("produrl", url_handler))
    application.add_handler(CommandHandler("url", url_handler))
    application.add_handler(CommandHandler("deploy", deploy_handler))
    application.add_handler(CommandHandler("screenshot", screenshot_handler))
    application.add_handler(MessageHandler(filters.ALL, message_handler))

    application.run_polling()


state = f"🌐🔒 Загружен продовый URL {DEFAULT_URL}"
driver = None
