import json
import logging
import pprint
import inflection
import pystache


def generate_client_code(schema_file):
    with open(schema_file, "r") as file:
        schema_data = json.load(file)

    client_template = """
# ... Код клиента на основе GraphQL schema.json
from sgqlc.types import ContainerTypeMeta, non_null
from schema import *
from graphql.client import GraphQLClient
from graphql.errors import GraphQLClientError


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
        json_data = response.get('data', {}).get(query_name)
        if json_data:
            return model(json_data)
        raise GraphQLClientError(response)

    {{#types}}
    {{#fields}}
    def {{field_name}}(self, {{arguments}}) -> {{response_model}} | dict:
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

    # map_types = {
    #     'String': 'str',
    #     'Boolean': 'bool',
    #     'Integer': 'int',
    #     'UUID': 'str'
    # }

    for type_data in schema_data["data"]["__schema"]["types"]:
        query_type = type_data.get('name')
        if query_type in ('Mutation', 'Query'):
            fields = []
            for field in type_data["fields"]:

                # args_types = [
                #     {
                #         inflection.underscore(arg["name"]): map_types.get(arg['type']['name'], arg['type']['name']) or
                #                                             map_types[arg['type']['ofType']['name']]
                #     } for arg in field.get("args", [])
                # ]

                args_types = [
                    {
                        inflection.underscore(arg["name"]): arg['type']['name'] or arg['type']['ofType']['name']
                    } for arg in field.get("args", [])
                ]
                merged_dict = {}

                for dictionary in args_types:
                    merged_dict.update(dictionary)

                args = [inflection.underscore(arg["name"]) for arg in field.get("args", [])]
                arguments = ", ".join([f'{k}: {v}' for k, v in merged_dict.items()])
                response_model = field.get('type').get('name') or 'non_null(MutationResult)'
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

    client_code = pystache.render(client_template, client_context)

    return client_code


schema_file = "schema.json"

client_code = generate_client_code(schema_file)

print("Код клиента на основе schema.json:")

with open('result.py', 'w') as file:
    file.write(client_code)
