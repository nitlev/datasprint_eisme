from urllib.parse import urlencode

import requests


def read_url(filename):
    with open(filename, "r") as url:
        return url.read()


class SlideSearchClient(object):
    def __init__(self):
        self.base_url = read_url("awsinstance")
        self.session = requests.Session()
        try:
            self.session.get(self.base_url)
        except requests.exceptions.ConnectionError:
            print("Couldn't connect :/ Are you sure the domain is correct ?")
            raise

    def search(self, query):
        url = self.search_url(query)
        return Documents(
            self.session.get(url).json().get("result", {}).get("results", [])
        )

    def search_url(self, query):
        url = self.base_url
        route = "/previews/search/api"
        encoded_query = urlencode({'q': query})
        return url + route + '?' + encoded_query

    def preview(self, document):
        url = self.preview_url(document)
        return self.session.get(url)

    def preview_url(self, document):
        url = self.base_url
        route = "/document/pdf"
        encoded_query = urlencode(
            {'document_signature': document.documentSignature}
        )
        encoded_page = urlencode({'page': document.page})
        return url + route + '?' + encoded_query + '#' + encoded_page


class Documents(object):
    def __init__(self, records):
        self.list = [Document(record) for record in records]

    def best_n(self, n):
        return sorted(self.list, key=lambda x: x.pertinence, reverse=True)[:n]


class Document(object):
    def __init__(self, dictionary):
        self.documentPath = dictionary.get("documentPath")
        self.documentFileName = dictionary.get("documentFileName")
        self.page = dictionary.get("page")
        self.documentSignature = dictionary.get("documentSignature")
        self.pertinence = dictionary.get("pertinence")
        self.id = dictionary.get("id")
