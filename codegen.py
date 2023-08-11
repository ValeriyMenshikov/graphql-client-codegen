import json
import logging
import pprint
import inflection
import pystache


def generate_client_code(schema_file):
    with open(schema_file, "r") as file:
        schema_data = json.load(file)

    # Генерация кода клиента
    client_template = """
# ... Код клиента на основе GraphQL schema.json
class GraphQLApiClient:
    def __init__(self, host: str, headers: dict = None, disable_log: bool = False):
        self.host = host
        self.headers = headers
        self.disable_log = disable_log
        self.client = GraphQLClient(
            host=self.host,
            schema=schema,
            base_headers=self.headers,
            disable_log=self.disable_log
        )

    @staticmethod
    def _convert_to_model(response: dict, query_name: str, model: ContainerTypeMeta):
        '''
        Метод преобразует json dict ответ в соответсвующую ResponseModel, в противном случае отдает
        полный json dict
        :param response: GraphQL response
        :param query_name: mutation or query name
        :param model: GraphQL response model from schema
        :return:
        '''
        json_data = response.get('data', {}).get(query_name)
        if json_data:
            return model(json_data)
        raise GraphQLClientError(response)

    {{#types}}
    {{#fields}}
    def {{field_name}}(self, {{arguments}}) -> {{response_model}}:

        query_name = '{{query_name}}'
        {{operation_type}} = self.client.{{operation_type}}(name=query_name)
        {{operation_type}}.{{field_name}}(
        {{#args}}
            {{.}}={{.}},
        {{/args}}
        )
        
        response = self.client.request(query={{operation_type}})

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model={{response_model}}
        )
        return response

    {{/fields}}
    {{/types}}
    """

    client_context = {
        "types": []
    }

    for type_data in schema_data["data"]["__schema"]["types"]:
        query_type = type_data.get('name')
        if query_type in (
                'Mutation',
                'Query',
        ):
            fields = []
            for field in type_data["fields"]:
                pprint.pprint(field)
                args = [inflection.underscore(arg["name"]) for arg in field.get("args", [])]
                arguments = ", ".join(args)
                response_model = field.get('type').get('name') or 'sgqlc.types.non_null(MutationResult)'
                fields.append({
                    "field_name": inflection.underscore(field["name"]),
                    "query_name": field["name"],
                    "arguments": arguments,
                    "response_model": response_model,
                    "operation_type": 'query' if query_type == 'query' else 'mutation',
                    "args": args

                })

            client_context["types"].append({
                "type_name": type_data["name"],
                "fields": fields,
            })

    # pprint.pprint(client_context)
    client_code = pystache.render(client_template, client_context)

    return client_code


def generate_tests_code(schema_file):
    with open(schema_file, "r") as file:
        schema_data = json.load(file)

    # Генерация кода автотестов
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

    tests_context = {
        "types": [],
        "endpoint": "https://example.com/graphql"
    }

    for type_data in schema_data["data"]["__schema"]["types"]:
        if type_data["kind"] == "OBJECT":
            fields = []
            for field in type_data["fields"]:
                fields.append({
                    "field_name": field["name"]
                })

            tests_context["types"].append({
                "type_name": type_data["name"],
                "fields": fields
            })

    tests_code = pystache.render(tests_template, tests_context)

    return tests_code


# Использование
schema_file = "schema.json"

client_code = generate_client_code(schema_file)
tests_code = generate_tests_code(schema_file)

print("Код клиента на основе schema.json:")

with open('result.py', 'w') as file:
    file.write(client_code)
print(client_code)

print("\nКод автотестов на основе schema.json:")
# print(tests_code)
