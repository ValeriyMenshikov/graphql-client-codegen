import json
import pprint
import inflection
import pystache
from graphql_codegen.internal.templates.client_template import client_template
from graphql_codegen.internal.templates.tests_template import tests_template
from graphql_codegen.internal.templates.test_template import test_template


def get_args_and_types(args):
    args_and_types = {}
    for arg in args:
        arg_name = inflection.underscore(arg["name"])
        arg_type = arg['type']['name'] or arg['type']['ofType']['name']
        args_and_types[arg_name] = arg_type
    return args_and_types


def parse_shema_json(schema_file):
    with open(schema_file, "r") as file:
        schema_data = json.load(file)

    params_object = {
        "types": []
    }

    for type_data in schema_data["data"]["__schema"]["types"]:
        query_type = type_data.get('name').lower()
        if query_type in ('mutation', 'query'):
            fields = []
            for field in type_data["fields"]:
                args = field.get("args", [])
                args_and_types = get_args_and_types(args)
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

    return params_object


def generate_client_library(params_object):
    """

    :param params_object:
    :return:
    """
    client_code = pystache.render(client_template, params_object)
    return client_code


def generate_tests(params_object):
    tests_code = pystache.render(tests_template, params_object)
    return tests_code


def generate_tests_dictionary(params_object):
    tests = {}
    for type in params_object['types']:
        for field in type['fields']:
            field_name = field['field_name']
            field['class_name'] = inflection.camelize(field_name)
            test_code = pystache.render(test_template, field)
            tests.update({field_name: test_code})
    return tests



