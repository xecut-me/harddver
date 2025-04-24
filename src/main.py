from http.server import HTTPServer, SimpleHTTPRequestHandler
from dverchrome import start_chrome
from dvertg import start_bot
import threading
import signal
import sys


def cleanup(signum, frame):
    driver.quit()
    sys.exit(0)


def run_http_server():
    httpd = HTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler(directory="./static/"))
    httpd.serve_forever()


threading.Thread(target=run_http_server, daemon=True).start()

driver = start_chrome()

with open("./chat.json.log", "r") as file:
    for line in file:
        driver.execute_script("addMessage(arguments[0]);", line)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

start_bot(driver)
