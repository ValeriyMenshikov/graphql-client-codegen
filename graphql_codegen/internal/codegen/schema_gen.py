import os
import time
from pathlib import Path
from graphql_codegen.internal.codegen.utils import run_command
from graphql_codegen import logger


class SchemaGen:
    SCHEMA_FILENAME = "schema.json"
    SGQLC_TYPES_FILENAME = "schema.py"

    def __init__(self, url, output):
        self.url = url
        self.output = Path(output)
        self.json_schema = self.output.joinpath(self.SCHEMA_FILENAME)

    def _create_directory(self):
        self.output.mkdir(exist_ok=True)
        self.output.joinpath('__init__.py').touch()

    def get_schema(self):
        logger.info(f'Get json schema from: {self.url}')
        self._create_directory()
        command = fr'''python3 -m sgqlc.introspection --exclude-deprecated --exclude-description %s %s''' % (
            self.url,
            self.json_schema
        )
        run_command(command)
        return self.json_schema

    def generate_sgql_types(self):
        logger.info(f'Generate sgql types from: {self.json_schema}')
        """
        Example:

        gen_schema(schema.json, schema.py)

        :param json_schema:
        :param destination_path:
        :return:
        """
        sgql_types_file_path = self.output.joinpath(self.SGQLC_TYPES_FILENAME)
        self.get_schema()
        command = fr'''sgqlc-codegen schema {self.json_schema} {sgql_types_file_path}'''
        run_command(command)
        return sgql_types_file_path
