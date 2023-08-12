test_template = """from ..graphql_client.schema import *


class Tests{{class_name}}:

    def test_{{field_name}}(self, client):
        # Заполни тестовые данные
        {{#test_args}}
        {{.}} = None
        {{/test_args}}
        response = client.{{field_name}}(
            {{#args}}
            {{.}}={{.}},
            {{/args}}
        )
        assert response

"""