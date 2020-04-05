from modules.module import Module


class Course(Module):
    NAME = "Course"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)

    def handle(self, content):
        Module.handle(self, content)
        if not content:
            pass

        self._enqueue_response(self._content["exit"])
        self._send()
