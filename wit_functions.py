class MockWitClient(object):
    def __init__(self):
        pass

    def message(self, message):
        return {'entities': {},
                'msg_id': 'acoolmessageid',
                '_text': "Bot received '{}'".format(message)}


def send_message_to_client(client, message):
    return client.message(message)
