import json
import logging
import pprint
import inflection
import pystache
from graphql_codegen.templates.client_template import client_template
from graphql_codegen.templates.tests_template import tests_template


def generate_client_code(schema_file):
    with open(schema_file, "r") as file:
        schema_data = json.load(file)

    client_context = {
        "types": []
    }

    for type_data in schema_data["data"]["__schema"]["types"]:
        query_type = type_data.get('name').lower()
        if query_type in ('mutation', 'query'):
            fields = []
            for field in type_data["fields"]:
                args = field.get("args", [])
                args_and_types = {}
                for arg in args:
                    arg_name = inflection.underscore(arg["name"])
                    arg_type = arg['type']['name'] or arg['type']['ofType']['name']
                    args_and_types.update({arg_name: arg_type})

                args1 = args_and_types.keys()
                arguments = ", ".join([f'{k}: {v}' for k, v in args_and_types.items()])

                response_model = field.get('type').get('name') or f"non_null({field.get('type').get('ofType').get('name')})"
                fields.append({
                    "field_name": inflection.underscore(field["name"]),
                    "query_name": field["name"],
                    "arguments": arguments,
                    "response_model": response_model,
                    "operation_type": query_type,
                    "args": args1
                })
            client_context["types"].append({
                "type_name": type_data["name"],
                "fields": fields,
            })

    client_code = pystache.render(client_template, client_context)

    return client_code


def generate_tests_code(schema_file):
    with open(schema_file, "r") as file:
        schema_data = json.load(file)

    # Генерация кода автотестов

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
