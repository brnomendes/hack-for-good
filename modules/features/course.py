from flask import session
from modules.module import Module


class Course(Module):
    NAME = "Course"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)

        self._current_module_key = f"{self.NAME}-module"
        self._current_session_key = f"{self.NAME}-session"

    def clear(self):
        if self._current_module_key in session:
            session.pop(self._current_module_key)
        if self._current_session_key in session:
            session.pop(self._current_session_key)

    def handle(self, content):
        Module.handle(self, content)

        current_module = session.get(self._current_module_key, None)

        if not current_module:
            if content is None:
                self._welcome()
            elif content not in ["1", "2"]:
                self._enqueue_generic(self._content["menu"])
            else:
                self._run_module(content, current_module)
        else:
            self._run_module(content, current_module)

        self._send()

    def _run_module(self, content, current_module):
        if not current_module:
            session[self._current_session_key] = 0
            if content == "1":
                session[self._current_module_key] = "module_1"
            else:
                session[self._current_module_key] = "module_2"

            self._enqueue_session()
            return

        current_session = int(session.get(self._current_session_key))
        current_session = current_session + 1
        if current_module == "module_2" and current_session >= len(
            self._content["module_2"]
        ):
            self._enqueue_generic(self._content["exit"])
            return

        if content != "1":
            self._enqueue_generic(self._content["continue"])
            return

        if current_module == "module_1" and current_session >= len(
            self._content["module_1"]
        ):
            current_session = 0
            current_module = "module_2"

        session[self._current_session_key] = current_session
        session[self._current_module_key] = current_module
        self._enqueue_session()

    def _enqueue_session(self):
        m = session[self._current_module_key]
        s = int(session[self._current_session_key])
        for content in self._content[m][s]:
            self._enqueue_generic(content)
        self._enqueue_generic(self._content["continue"])

    def _welcome(self):
        for message in self._content["welcome"]:
            self._enqueue_generic(message)
        self._enqueue_generic(self._content["menu"])

    def _enqueue_generic(self, content):
        if content.split(".")[-1] in ["mp3", "jpg", "jpeg"]:
            self._enqueue_response_media(self._get_static_file(content, self.NAME))
        else:
            self._enqueue_response(content)
