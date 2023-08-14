import inflection
import pystache
from graphql_codegen import logger
from graphql_codegen.internal.codegen.parser import _JsonSchemaParser
from graphql_codegen.internal.templates.client_template import client_template
from graphql_codegen.internal.templates.tests_template import tests_template
from graphql_codegen.internal.templates.test_template import test_template
import inflection


class GraphQLCodegen(_JsonSchemaParser):
    def __init__(self, json_schema, service_name):
        self.service_name = service_name
        super().__init__(json_schema)
        self.params['service_name'] = inflection.camelize(service_name)

    def generate_client_library(self):
        logger.info(f'Generate python client code')
        client_code = pystache.render(client_template, self.params)
        return client_code

    def generate_tests(self):
        logger.info(f'Generate all tests code in file')
        tests_code = pystache.render(tests_template, self.params)
        return tests_code

    def generate_tests_dictionary(self):
        logger.info(f'Generate code for each test')
        tests = {}
        for type in self.params['types']:
            for field in type['fields']:
                field_name = field['field_name']
                field['class_name'] = inflection.camelize(field_name)
                test_code = pystache.render(test_template, field)
                tests.update({field_name: test_code})
        return tests
