conftest_template = """import pytest

from ..{{module_name}} import GraphQL{{service_name}}Client
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def client():
    return GraphQL{{service_name}}Client(host='{{url}}')
"""
