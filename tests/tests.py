from app import hello_world


class TestClass:
    def test_hello_world_should_return_helloworld(self):
        # Given
        #

        # When
        resp = hello_world()

        # Assert
        assert resp == "Hello World!"
