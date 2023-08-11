tests_template = """import structlog

from schema import *

class TestsHandlers:

    {{#types}}
    {{#fields}}
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
        
    {{/fields}}
    {{/types}}

"""
