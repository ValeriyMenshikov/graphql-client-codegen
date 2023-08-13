from graphql_codegen.internal.codegen.codegen import parse_shema_json, generate_client_library, generate_tests


def test_parse_json_schema():
    parameter_object = parse_shema_json(schema_file='../schema.json')
    result = generate_client_library(parameter_object)

    print(result)

    tests = generate_tests(params_object=parameter_object)
    print(tests)
