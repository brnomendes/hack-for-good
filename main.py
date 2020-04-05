from handler import handle_messages
from sender import Sender

import uuid
import logging
import os

from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, render_template
from flask_socketio import SocketIO

NAME = "QUARENTENA-SE"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", uuid.uuid4().hex)
SOCKETIO = SocketIO(app)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(NAME)


@app.route("/twilio", methods=["POST"])
def entry_point():
    if "From" in request.form and "Body" in request.form:
        LOGGER.info(f"NEW MESSAGE {request.form['From']}: {request.form['Body']}")
        # try:
        handle_messages(request.form["From"], request.form["Body"].strip())
        # except Exception as e:
        #     LOGGER.error(e)

    return str(MessagingResponse())


@app.route("/status", methods=["POST"])
def update_status():
    if "To" in request.form and "MessageStatus" in request.form:
        LOGGER.info(
            f"STATUS UPDATE {request.form['To']}: {request.values['MessageStatus']}"
        )
        try:
            sender = Sender(request.form["To"])
            sender.update(request.values["MessageStatus"])
        except Exception as e:
            LOGGER.error(e)

    return str(MessagingResponse())


@app.route("/", methods=["GET"])
def admin_page():
    return render_template("admin.html")


if __name__ == "__main__":
    SOCKETIO.run(app, debug=True)
