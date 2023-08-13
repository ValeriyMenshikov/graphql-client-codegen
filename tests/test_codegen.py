from graphql_codegen.internal.codegen.codegen import parse_shema_json, generate_tests, generate_client_library

schema_file = "../schema.json"


def test_client_codegen():
    params_object = parse_shema_json(schema_file)

    with open('../graphql_api.py', 'w') as file:
        file.write(generate_client_library(params_object))

    with open('../tests_handlers.py', 'w') as file:
        file.write(generate_tests(params_object))