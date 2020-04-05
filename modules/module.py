from flask_socketio import emit
from flask import request
import requests


class Module:
    def __init__(self, sender, number):
        self._sender = sender
        self.number = number
        self._content = self._get_content(self.NAME)

    def handle(self, content):
        self._emit_event(content)

    def _enqueue_response(self, content):
        self._sender._enqueue_response(content)

    def _enqueue_response_media(self, url):
        self._sender._enqueue_response_media(url)

    def _send(self):
        self._sender._send_next()

    def _emit_event(self, content):
        if content != None:
            emit(
                "twilio",
                {"number": self.number, "content": content, "as_send": False},
                broadcast=True,
                namespace="/",
            )

    def _get_content(self, name):
        content = self.get_contents()
        return content["modules"][name]

    @staticmethod
    def get_contents():
        url = Module._get_static_file("content.json")

        return requests.get(url).json()

    @staticmethod
    def _get_static_file(filename, module_name=None):

        if module_name:
            return f"{request.url_root}/static/{module_name}/{filename}"
        else:
            return f"{request.url_root}/static/{filename}"
