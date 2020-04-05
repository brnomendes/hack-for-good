from flask import session
from modules.module import Module


class Message(Module):
    NAME = "Message"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)
        self._last_message_key = f"{self.NAME}-message"

    def handle(self, content):
        Module.handle(self, content)

        index = session.get(self._last_message_key, 0)
        index = index + 1

        messages = self._content["messages"]
        m = messages[index % len(messages)]
        self._enqueue_response(m["text"])
        self._enqueue_response_media(
            self._get_static_file(m["image"], self.NAME)
        )
        self._enqueue_response(self._content["source"])

        session[self._last_message_key] = index

        self._enqueue_response(self._content["exit"])
        self._send()
