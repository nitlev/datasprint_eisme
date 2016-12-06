from app.slidesearch_client import Documents
from app.wit_client import best_entity_value, build_url_from_document, \
    search_with_client


class MockWitClient(object):
    def __init__(self):
        pass

    def message(self, message):
        return {'entities': {},
                'msg_id': 'acoolmessageid',
                '_text': "Bot received '{}'".format(message)}


class MockSlideSearchClient(object):
    def __init__(self):
        pass

    def search(self, query):
        return Documents([{"documentFileName": "foo",
                           "documentPath": "/foo",
                           "page": 1,
                           "documentSignature": "bar",
                           "pertinence": 1,
                           "id": "kagabndao"}])

    def preview_url(self, document):
        return "preview_mock"


class TestClass:
    def test_best_entity_value_should_return_None_when_no_entities_are_found(
            self):
        # Given
        entities = []

        # When
        best_value = best_entity_value(entities)

        # Assert
        assert best_value is None

    def test_best_entity_value_should_return_best_value(self):
        # Given
        entities = [{'confidence': 0.8, "value": 'a'},
                    {'confidence': 0.9, "value": 'b'},
                    {'confidence': 0.7, "value": 'c'}]

        # When
        best_value = best_entity_value(entities)

        # Assert
        assert best_value == 'b'

    def test_search_should_update_context_with_link(self):
        # Given
        entities = {"search_query": [{'confidence': 0.8, "value": 'a'}]}
        request = {"context": {}, "entities": entities}
        mock_slide_search_client = MockSlideSearchClient()

        # When
        new_context = search_with_client(mock_slide_search_client)(request)

        # Assert
        assert 'link' in new_context.keys()

    def test_build_link_from_query_with_one_word(self):
        # Given
        query = "foo"
        mock_slide_search_client = MockSlideSearchClient()
        doc = mock_slide_search_client.search(query)

        # When
        link = build_url_from_document(mock_slide_search_client, doc)

        # Assert
        assert link == "cool_stuff_about_foo.io"

    def test_build_link_from_query_with_two_word(self):
        # Given
        query = "foo bar"
        mock_slide_search_client = MockSlideSearchClient()
        doc = mock_slide_search_client.search(query)

        # When
        link = build_url_from_document(mock_slide_search_client, doc)

        # Assert
        assert link == "cool_stuff_about_foo_bar.io"
