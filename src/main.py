from dverhttp import run_http_server
from dverchrome import start_chrome
from dvertg import start_bot
import threading
import signal
import sys


def cleanup(signum, frame):
    driver.quit()
    sys.exit(0)


threading.Thread(target=run_http_server, daemon=True).start()

driver = start_chrome()

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

start_bot(driver)
