import json

from flask import Flask
from flask import request
from wit import Wit

from wit_functions import send_message_to_client


def read_token():
    with open("access_token", 'r') as token_file:
        token = token_file.read()
        return token


client = Wit(read_token())
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/message', methods=['POST'])
def send_message():
    message = request.get_json().get("message", "")
    return json.dumps(send_message_to_client(client, message))


if __name__ == '__main__':
    app.run()
