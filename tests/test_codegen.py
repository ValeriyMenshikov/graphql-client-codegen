from graphql_codegen.codegen import generate_client_code

schema_file = "../schema.json"


def test_client_codegen():
    client_code = generate_client_code(schema_file)
    with open('../graphql_api.py', 'w') as file:
        file.write(client_code)
