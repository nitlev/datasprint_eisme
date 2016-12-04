from wit_functions import MockWitClient, send_message_to_client


class TestClass:
    def test_send_message_should_return_bot_message(self):
        # Given
        client = MockWitClient()
        message = "Bonjour !"

        # When
        response = send_message_to_client(client, message)

        # Assert
        assert response['_text'] == "Bot received 'Bonjour !'"
