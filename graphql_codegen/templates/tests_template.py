tests_template = """
    import logging
    import unittest
    from graphql_client import GraphQLClient

    class GraphQLTests(unittest.TestCase):
        def setUp(self):
            self.client = ... GraphQLClient("{{endpoint}}")
            self.logger = logging.getLogger(__name__)

        {{#types}}
        {{#fields}}
        def test_{{field_name}}(self):
            # Создание запроса
            # Вызов метода клиента
            # Проверка результата
            pass
        {{/fields}}
        {{/types}}

    if __name__ == "__main__":
        unittest.main()
    """