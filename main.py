from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from secret import SECRET_TELEGRAM_API_KEY, BACKDOOR_AUTH, BACKDOOR_URL
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from telegram import Update
import subprocess
import functools
import threading
import socket
import signal
import json
import sys
import os


class MyHTTPHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/secrets":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {"BACKDOOR_AUTH": BACKDOOR_AUTH, "BACKDOOR_URL": BACKDOOR_URL}
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            super().do_GET()


def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.forward_from or update.message.forward_from_chat:
            return
        
        if update.effective_chat.id != admin_chat_id:
            await update.message.reply_text(no_auth_msg)
            return
        
        await func(update, context)
    return wrapper


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = json.dumps(update.to_dict(), ensure_ascii=False)

    try:
        response = driver.execute_script("return onMessage(arguments[0]);", message)
    except Exception as e:
    
        print(f"JS error: {e}")
        response = None
    
    if response:
        await update.message.reply_text(response)


@admin_only
async def reload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    driver.refresh()
    await update.message.reply_text("🔄 Страница перезагружена " + state)


@admin_only
async def produrl_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    driver.get(DEFAULT_URL)
    state = f"🌐🔒 Загружен продовый URL {DEFAULT_URL}"
    await update.message.reply_text(state)


@admin_only
async def url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        custom_url = context.args[0]
        driver.get(custom_url)
        state = f"🌐🧪 Загружен тестовый URL {custom_url}"
        await update.message.reply_text(state)
    else:
        state = f"🌐🔒 Загружен продовый URL {DEFAULT_URL}"
        await update.message.reply_text(state)


@admin_only
async def deploy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subprocess.run(["git", "pull"])
    await update.message.reply_text("🚀 git pull = ok")

    driver.quit()
    await update.message.reply_text("🚀 driver.quit() = ok, крешимся для перезапуска супервизором 😂")
    
    sys.exit(0)


async def init(app: Application) -> None:
    thread = threading.Thread(target=run_http_server, daemon=True)
    thread.start()

    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    commit_hash = result.stdout.strip()
    
    await application.bot.send_message(chat_id=admin_chat_id, text=f"🎉 Я запустился! Версия https://github.com/xecut-me/harddver/tree/{commit_hash}")


def cleanup(signum, frame):
    driver.quit()
    sys.exit(0)


def is_vnc_port_taken(host='127.0.0.1', port=5900):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True


def run_http_server():
    handler_class = functools.partial(MyHTTPHandler, directory="./static/")
    httpd = HTTPServer(("127.0.0.1", 8000), handler_class)
    httpd.serve_forever()






admin_chat_id = -1002571293789
no_auth_msg = "Это админская команда, работает только в чате https://t.me/+IBkZEqKkqRlhNGQy"
DEFAULT_URL = "http://127.0.0.1:8000/"
state = f"🌐🔒 Загружен продовый URL {DEFAULT_URL}"


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


# subprocess.run(["killall", "-9", "chrome"])
# subprocess.run(["killall", "-9", "chromedriver"])

os.environ["DISPLAY"] = ":0"
options = Options()

if not is_vnc_port_taken():
    options.add_argument("--kiosk")

options.add_argument("--no-first-run")
options.add_argument("--disable-infobars")
options.add_argument("--noerrdialogs")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
driver.get(DEFAULT_URL)


application: Application = Application.builder().token(SECRET_TELEGRAM_API_KEY).post_init(init).build()

application.add_handler(CommandHandler("reload", reload_handler))
application.add_handler(CommandHandler("produrl", produrl_handler))
application.add_handler(CommandHandler("url", url_handler))
application.add_handler(CommandHandler("deploy", deploy_handler))
application.add_handler(MessageHandler(filters.ALL, message_handler))

application.run_polling()
