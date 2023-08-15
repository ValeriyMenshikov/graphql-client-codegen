from graphql_codegen.internal.codegen.codegen import GraphQLCodegen
from graphql_codegen.internal.codegen.schema_gen import SchemaGen
from graphql_codegen.internal.codegen.utils import write_code_to_file, create_directory
from pathlib import Path


def run(url, output_dir, service_name, make_tests):
    # Создание пакета
    schema = SchemaGen(url=url, output=output_dir)
    schema.generate_sgql_types()
    codegen = GraphQLCodegen(json_schema=schema.json_schema, service_name=service_name, url=url)
    client_code_text = codegen.generate_client_library()
    write_code_to_file(file_path=Path(output_dir).joinpath(f'{service_name}.py'), content=client_code_text)

    # Генерация тестов
    if make_tests:
        conftest = codegen.generate_conftest()
        tests = codegen.generate_tests_dictionary()
        write_tests(tests=tests, output_dir=output_dir, conftest=conftest)


def write_tests(tests, output_dir, conftest):
    path = Path(output_dir).joinpath('tests')
    tests_dir = create_directory(path)
    write_code_to_file(file_path=tests_dir.joinpath('conftest.py'), content=conftest)

    for name, code in tests.items():
        test_path = tests_dir.joinpath(f"test_{name}.py")
        write_code_to_file(test_path, code)
