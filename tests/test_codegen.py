from graphql_codegen.internal.codegen.codegen import parse_graphql_json_schema, gen_tests_code, gen_client_code

schema_file = "../schema.json"


def test_client_codegen():
    params_object = parse_graphql_json_schema(schema_file)

    with open('../graphql_api.py', 'w') as file:
        file.write(gen_client_code(params_object))

    with open('../tests_handlers.py', 'w') as file:
        file.write(gen_tests_code(params_object))