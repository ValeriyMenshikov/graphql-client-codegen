from graphql_codegen.internal.codegen.codegen import parse_graphql_json_schema, gen_client_code, \
    gen_tests_in_other_files
from graphql_codegen.internal.codegen.schema_gen import get_schema, generate_schema
from pathlib import Path


def create_init_file(directory):
    Path(directory.joinpath("__init__.py")).touch()


def create_file_with_content(file_path, content):
    Path(file_path).write_text(content)


def run(url, output_dir, make_tests):
    # Создание пакета
    destination_path = Path(output_dir)
    destination_path.mkdir(exist_ok=True)
    create_init_file(destination_path)

    # Получение json схемы и создание пакета с клиентом и схемой
    schema_json = destination_path.joinpath("schema.json")
    graphql_package = destination_path.joinpath("graphql_client")

    graphql_package.mkdir(exist_ok=True)
    create_init_file(graphql_package)

    get_schema(url=url, destination_path=schema_json)
    generate_schema(json_schema=schema_json, destination_path=f"{graphql_package}/schema.py")

    params_object = parse_graphql_json_schema(schema_file=schema_json)
    client = gen_client_code(params_object)

    create_file_with_content(f"{graphql_package}/graphql_api.py", client)

    # Генерация тестов
    if make_tests:
        create_tests(destination_path, params_object)


def create_tests(destination_path, params_object):
    all_tests_in_another_files = gen_tests_in_other_files(params_object)
    tests_dir = destination_path.joinpath("tests")
    tests_dir.mkdir(exist_ok=True)
    create_init_file(tests_dir)

    for name, code in all_tests_in_another_files.items():
        test_path = tests_dir.joinpath(f"test_{name}.py")
        create_file_with_content(test_path, code)


if __name__ == '__main__':
    run(url='http://localhost:5051/graphql', output_dir='./client', make_tests=True)
