from modules.module import Module

import json
import random

from flask import session
import feedparser
import hashlib


class News(Module):
    NAME = "News"

    def __init__(self, sender, number):
        Module.__init__(self, sender, number)
        self._sended_news_key = f"{self.NAME}-sended"
        self._needs = ["coronavirus", "coronavírus", "covid", "quarentena"]
        self._max_attempts = 50

    def handle(self, content):
        Module.handle(self, content)

        sended = json.loads(session.get(self._sended_news_key, "[]"))

        to_send = None
        attempts = 0
        while not to_send:
            try:
                new = self._get_new()
            except Exception:
                pass

            if new:
                to_send_hash = hashlib.md5(new["link"].encode()).hexdigest()
                if to_send_hash not in sended:
                    to_send = new
                    sended.append(to_send_hash)

            attempts = attempts + 1
            if attempts >= self._max_attempts:
                break

        if to_send:
            session[self._sended_news_key] = json.dumps(sended)
            self._enqueue_response(to_send["title"])
            self._enqueue_response(to_send["link"])
        else:
            self._enqueue_response(self._content["not_found"])

        self._enqueue_response(self._content["exit"])
        self._send()

    def _get_new(self):
        url = random.choice(self._content["feeds"])
        feed = feedparser.parse(url)
        item = random.choice(feed["entries"])
        if item and "title" in item and "description" in item and "link" in item:
            for word in self._needs:
                if word in item["title"] or word in item["description"]:
                    return item

        return None
