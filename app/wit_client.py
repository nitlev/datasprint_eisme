from operator import itemgetter

from flask_sse import sse


def best_entity_value(entities):
    """
    Returns highest ranked entity value
    """
    if len(entities) == 0:
        return None
    else:
        sorted_entities = sorted(entities,
                                 key=itemgetter("confidence"),
                                 reverse=True)
        val = sorted_entities[0].get('value', None)
        return val


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
    query = best_entity_value(entities.get('search_query', []))
    context['link'] = "cool_stuff_about_{}.io".format(query)
    return context


actions = {
    'send': send,
    'search': search
}

