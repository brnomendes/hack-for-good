from flask_socketio import emit
from twilio.rest import Client
import redis
import json
import os


class Sender:
    def __init__(self, number):
        self._number = number
        self._queue = redis.from_url(os.getenv("REDIS_URL"))
        self._account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self._auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self._origin_number = os.getenv("TWILIO_ORIGIN_NUMBER")

        self._client = Client(self._account_sid, self._auth_token)

    def _enqueue_response(self, content):
        self._enqueue({"text": content})

    def _enqueue_response_media(self, url):
        self._enqueue({"media": url})

    def _emit_event(self, content):
        if content != None:
            emit(
                "twilio",
                {"number": self._number, "content": content, "as_send": True},
                broadcast=True,
                namespace="/",
            )

    def _enqueue(self, content):
        self._queue.rpush(self._number, json.dumps(content))

    def update(self, status):
        if status in ["delivered", "failed", "undelivered"]:
            self._send_next()

    def _send_next(self):
        if self._queue.llen(self._number) > 0:
            raw = self._queue.lpop(self._number)
            if not raw:
                return

            content = json.loads(raw)

            self._client.messages.create(
                body=content.get("text", None),
                media_url=content.get("media", None),
                from_=f"whatsapp:{self._origin_number}",
                to=self._number,
            )

            if "text" in content:
                self._emit_event(content["text"])
            if "media" in content:
                self._emit_event(content["media"])
