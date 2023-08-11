from graphql_codegen.internal.codegen.codegen import parse_graphql_json_schema, gen_client_code, \
    gen_tests_in_other_files
from graphql_codegen.internal.codegen.schema_gen import get_schema, generate_schema
from pathlib import Path


def run(url, output_dir):

    destination_path = Path(output_dir).parent.joinpath('schema.json')
    graphql_package = Path(output_dir).parent.joinpath('graphql_client')
    graphql_package.mkdir(exist_ok=True)
    with open(f'{graphql_package.joinpath("__init__.py")}', 'w'): ...

    get_schema(url=url, destination_path=destination_path)
    generate_schema(json_schema=destination_path, destination_path=f'{graphql_package}/schema.py')
    params_object = parse_graphql_json_schema(schema_file=destination_path)
    client = gen_client_code(params_object)
    all_tests_in_another_files = gen_tests_in_other_files(params_object)

    with open(f'{graphql_package}/graphql_api.py', 'w') as file:
        file.write(client)

    for name, code in all_tests_in_another_files.items():
        test_path = Path(output_dir).parent.joinpath('tests').joinpath(f'test_{name}.py')
        with open(f'{test_path}', 'w') as file:
            file.write(code)


run(url='http://localhost:5051/graphql', output_dir='../../')
