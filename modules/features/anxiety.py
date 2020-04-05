from modules.module import Module


class Anxiety(Module):
    NAME = "Anxiety"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)

    def handle(self, content):
        Module.handle(self, content)
        if not content:
            for content in self._content["introduction"]:
                self._enqueue_response(content)

            self._enqueue_response_media(
                self._get_static_file(self._content["image"], self.NAME)
            )

            self._enqueue_response_media(
                self._get_static_file(self._content["video"], self.NAME)
            )

            for content in self._content["contents"]:
                self._enqueue_response(content)

        self._enqueue_response(self._content["exit"])
        self._send()
