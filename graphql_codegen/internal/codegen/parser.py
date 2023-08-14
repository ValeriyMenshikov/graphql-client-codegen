import json

import inflection
from graphql_codegen import logger

class _JsonSchemaParser:
    def __init__(self, json_schema):
        self.json_schema = json_schema
        with open(json_schema) as file:
            self.schema = json.load(file)

        self.params = self._parse_schema_json()

    @staticmethod
    def _get_args_and_types(args):
        args_and_types = {}
        for arg in args:
            arg_name = inflection.underscore(arg["name"])
            arg_type = arg['type']['name'] or arg['type']['ofType']['name']
            args_and_types[arg_name] = arg_type
        return args_and_types

    def _parse_schema_json(self):
        logger.info(f'Parse json schema: {self.json_schema}')
        params_object = {
            "types": []
        }

        for type_data in self.schema["data"]["__schema"]["types"]:
            query_type = type_data.get('name').lower()
            if query_type in ('mutation', 'query'):
                fields = []
                for field in type_data["fields"]:
                    args = field.get("args", [])
                    args_and_types = self._get_args_and_types(args)
                    handler_args = args_and_types.keys()
                    arguments = ", ".join([f'{k}: {v}' for k, v in args_and_types.items()])
                    response_model = field['type']['name'] or f"non_null({field['type']['ofType']['name']})"
                    field_name = field["name"]
                    fields.append({
                        "field_name": inflection.underscore(field_name),
                        "query_name": field_name,
                        "arguments": arguments,
                        "response_model": response_model,
                        "operation_type": query_type,
                        "args": handler_args,
                        "test_args": list(map(str.strip, arguments.split(',')))
                    })
                params_object["types"].append({
                    "type_name": type_data["name"],
                    "fields": fields,
                })

        self.params = params_object
        return params_object
