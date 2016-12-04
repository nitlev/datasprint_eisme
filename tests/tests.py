from app.wit_client import best_entity_value, search


class MockWitClient(object):
    def __init__(self):
        pass

    def message(self, message):
        return {'entities': {},
                'msg_id': 'acoolmessageid',
                '_text': "Bot received '{}'".format(message)}


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

        # When
        new_context = search(request)

        # Assert
        assert 'link' in new_context.keys()
