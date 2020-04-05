from modules.module import Module


class Prevention(Module):
    NAME = "Prevention"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)

    def handle(self, content):
        Module.handle(self, content)
        if not content:
            for content in self._content["contents"]:
                self._enqueue_response(content)

        self._enqueue_response(self._content["exit"])
        self._send()
