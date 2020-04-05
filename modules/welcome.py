from modules.module import Module

from flask import session


class Welcome(Module):
    NAME = "Welcome"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)
        self._cookie_key = "welcome"

    def handle(self, content, menu):
        Module.handle(self, content)

        if self._cookie_key in session:
            for item in menu:
                if item["option"] == content:
                    return True

            self._enqueue_response(self._content["ask_again"])
        else:
            self._enqueue_response(self._content["welcome_message"])
            session[self._cookie_key] = True

        menu_text = "\n".join([f'{item["option"]} - {item["text"]}' for item in menu])
        self._enqueue_response(menu_text)
        self._enqueue_response(self._content["how_to_response"])
        self._send()
        return False
