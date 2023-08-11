from graphql_codegen.internal.codegen.codegen import parse_graphql_json_schema, gen_client_code, \
    gen_tests_in_other_files
from graphql_codegen.internal.codegen.schema_gen import get_schema, generate_schema
from pathlib import Path


def run(url, output_dir, only_client=True):
    destination_path = Path(output_dir)
    destination_path.mkdir(exist_ok=True)
    schema_json = destination_path.joinpath('schema.json')

    graphql_package = Path(output_dir).joinpath('graphql_client')
    graphql_package.mkdir(exist_ok=True)
    with open(f'{graphql_package.joinpath("__init__.py")}', 'w'):
        ...

    get_schema(url=url, destination_path=schema_json)
    generate_schema(json_schema=schema_json, destination_path=f'{graphql_package}/schema.py')
    params_object = parse_graphql_json_schema(schema_file=schema_json)
    client = gen_client_code(params_object)
    all_tests_in_another_files = gen_tests_in_other_files(params_object)

    with open(f'{graphql_package}/graphql_api.py', 'w') as file:
        file.write(client)

    if only_client is False:
        tests_dir = Path(output_dir).parent.joinpath('tests')
        tests_dir.mkdir(exist_ok=True)
        for name, code in all_tests_in_another_files.items():
            test_path = tests_dir.joinpath(f'test_{name}.py')
            with open(f'{test_path}', 'w') as file:
                file.write(code)


if __name__ == '__main__':
    run(url='http://localhost:5051/graphql', output_dir='./rrr')
