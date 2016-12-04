from operator import itemgetter

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


def best_entity_value(entities, entity):
    """
    Returns highest_ranked entity value
    """
    if entity not in entities:
        return None

    relevant_entities = entities[entity]
    sorted_entities = sorted(relevant_entities,
                             key=itemgetter("confidence"),
                             reverse=True)
    val = sorted_entities[0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def send(request, response):
    """
    Sender function
    """
    sse.publish({"message": response['text'].decode('utf-8')}, type='bot')


def search(request):
    print("searching...")
    context = request['context']
    entities = request['entities']
    print(entities)
    query = best_entity_value(entities, 'search_query')
    context['link'] = "cool_stuff_about_{}.io".format(query)
    return context

actions = {
    'send': send,
    'search': search
}

client = Wit(read_token(), actions=actions)

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
    sse.publish({"message": message}, type='user')

    response = send_message_to_client(client, message)
    print(response)
    return "OK"

if __name__ == '__main__':
    app.run()
