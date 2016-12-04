import json

from flask import Flask
from flask import render_template
from flask import request
from flask_sse import sse

from wit import Wit
from wit_functions import send_message_to_client


def read_token():
    with open("access_token", 'r') as token_file:
        token = token_file.read()
        return token


client = Wit(read_token())
app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hello')
def publish_hello():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"


@app.route('/message', methods=['POST'])
def send_message():
    message = request.get_json().get("message", "")
    return json.dumps(send_message_to_client(client, message))

if __name__ == '__main__':
    app.run()
