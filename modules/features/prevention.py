from flask import session
from modules.module import Module


class Prevention(Module):
    NAME = "Prevention"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)
        self._last_image_index_key = f"{self.NAME}-image"

    def handle(self, content):
        Module.handle(self, content)
        if not content:
            for content in self._content["contents"]:
                self._enqueue_response(content)
            
            index = session.get(self._last_image_index_key, 0)
            index = index + 1

            images = self._content["images"]
            self._enqueue_response_media(
                self._get_static_file(images[index % len(images)], self.NAME)
            )

            session[self._last_image_index_key] = index


        self._enqueue_response(self._content["exit"])
        self._send()
