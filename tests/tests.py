from app import hello_world
from wit_functions import MockWitClient, send_message_to_client


class TestClass:
    def test_hello_world_should_return_HelloWorld(self):
        # Given
        #

        # When
        resp = hello_world()

        # Assert
        assert resp == "Hello World!"

    def test_send_message_should_return_bot_message(self):
        # Given
        client = MockWitClient()
        message = "Bonjour !"

        # When
        response = send_message_to_client(client, message)

        # Assert
        assert response['_text'] == "Bot received 'Bonjour !'"
