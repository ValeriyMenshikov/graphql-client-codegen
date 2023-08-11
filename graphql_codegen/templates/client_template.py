client_template = """
# ... Код клиента на основе GraphQL schema.json
from sgqlc.types import ContainerTypeMeta, non_null
from schema import *
from graphql_codegen.base_client.client import GraphQLClient
from graphql_codegen.base_client.errors import GraphQLClientError


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