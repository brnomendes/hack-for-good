from modules.module import Module

from flask import session


class Command(Module):
    NAME = "Command"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)

    def handle(self, content):
        Module.handle(self, content)

        if content == self._content["exit"]["text"]:
            session.clear()
            self._enqueue_response(self._content["exit"]["response"])
            self._send()
