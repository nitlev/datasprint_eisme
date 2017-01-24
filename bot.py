from flask import Flask, render_template, request
from flask_sse import sse
from wit import Wit

from app.slidesearch_client import SlideSearchClient
from app.wit_client import send, search_with_client


def read_token():
    with open("access_token", 'r') as token_file:
        token = token_file.read()
        return token


slidesearchclient = SlideSearchClient()

actions = {
    'send': send,
    'search': search_with_client(slidesearchclient)
}

client = Wit(read_token(), actions=actions)

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/message', methods=['POST'])
def send_message():
    message = request.get_json().get("message", "")
    print("got message : {}".format(message))
    sse.publish({"message": message}, type='user')

    client.run_actions("foo", message, verbose=10)
    return "OK"


if __name__ == '__main__':
    app.run()
