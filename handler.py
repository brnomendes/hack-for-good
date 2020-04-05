from pydoc import locate
from flask import session
from modules.features.course import Course
from modules.module import Module
from modules.command import Command
from modules.welcome import Welcome
from sender import Sender

menu_cookie_key = "menu"
exit_menu_message = "0"


def handle_messages(number, content):
    sender = Sender(number)
    MENU = Module.get_contents()[menu_cookie_key]
    if content in [
        i["text"] for i in Module.get_contents()["modules"]["Command"].values()
    ]:
        # A command was received.
        module = Command(sender, number)
        module.handle(content)
        return

    if menu_cookie_key in session:
        # The user was on a feature.
        if content != exit_menu_message:
            option = session[menu_cookie_key]
            run_module(sender, MENU, option, number, content)
            return

        course = Course(sender, number)
        course.clear()
        session.pop(menu_cookie_key)

    # The user wasn't in any feature.
    module = Welcome(sender, number)
    has_option = module.handle(content, MENU)
    if has_option:
        run_module(sender, MENU, content, number, None)


def run_module(sender, MENU, option, number, content):
    for item in MENU:
        if item["option"] == option:
            session[menu_cookie_key] = option
            module_class = locate(item["module"])
            module = module_class(sender, number)
            module.handle(content)
