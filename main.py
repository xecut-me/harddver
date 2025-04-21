from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import threading

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--kiosk")
options.add_argument("--no-first-run")
options.add_argument("--disable-infobars")
options.add_argument("--noerrdialogs")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://xecut-me.github.io/harddver/")
threading.Event().wait()