import http.server
import socketserver
import os
from typing_extensions import override
from config import ADMIN_PORT
from logger import logger

# because the original log message sucks, and i want to use my own logger


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    @override
    def log_message(self, format, *args):
        message = format % args
        logger.info(message)


def serve_admin():
    dist_dir = os.path.join(os.path.dirname(__file__), 'admin-ui', 'dist')
    os.chdir(dist_dir)
    httpd = socketserver.TCPServer(
        ("", ADMIN_PORT), MyHttpRequestHandler)
    httpd.serve_forever()
