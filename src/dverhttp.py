from http.server import HTTPServer, SimpleHTTPRequestHandler
from secret import BACKDOOR_AUTH, BACKDOOR_URL
from dverco2 import get_co2_emitted
import subprocess
import functools
import requests
import json
import re


class MyHTTPHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/backdoor":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            data = requests.get(BACKDOOR_URL, headers={"Authorization": BACKDOOR_AUTH}).json()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path == "/temp":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            result = subprocess.run("sensors", capture_output=True, text=True)
            exp = re.search(r"\+[^ ]+", result.stdout)
            text_result = ""

            if exp:
                text_result = exp.group()

            self.wfile.write(text_result.encode("utf-8"))
        elif self.path == "/co2":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            self.wfile.write(get_co2_emitted().encode("utf-8"))
        else:
            super().do_GET()


def run_http_server():
    handler_class = functools.partial(MyHTTPHandler, directory="./static/")
    httpd = HTTPServer(("127.0.0.1", 8000), handler_class)
    httpd.serve_forever()
