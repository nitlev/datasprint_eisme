from operator import itemgetter

from flask_sse import sse

from app.slidesearch_client import SlideSearchClient


def send(request, response):
    """
    Sender function
    """
    sse.publish({"message": response['text'].decode('utf-8')}, type='bot')


def search_with_client(client):
    def search(request):
        context, entities = extract_context_and_entities(request)
        query = best_entity_value(entities.get('search_query', []))
        context['link'] = build_link_from_query(client, query)
        return context

    return search


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


def extract_context_and_entities(request):
    context = request['context']
    entities = request['entities']
    return context, entities


def build_link_from_query(client, query):
    documents = documents_from_query(client, query)
    urls = [build_url_from_document(client, document) for document in documents]
    links = html_links(documents, urls)
    return "<br>".join(links)


def html_links(documents, urls):
    return ["<a href='" + url + "'>" + document.documentFileName + "</a>" for
            document, url in zip(documents, urls)]


def documents_from_query(client, query):
    docs = client.search(query)
    return docs.best_n(n=3)


def build_url_from_document(client, document):
    url = client.preview_url(document)
    return url


slidesearchclient = SlideSearchClient()

actions = {
    'send': send,
    'search': search_with_client(slidesearchclient)
}
