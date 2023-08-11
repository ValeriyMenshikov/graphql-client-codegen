tests_template = """import pytest

from graphql_api import GraphQLApiClient
import structlog

from schema import *

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def client():
    return GraphQLApiClient(host='http://localhost:5051/graphql')
"""