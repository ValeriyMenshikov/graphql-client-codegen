# graphql-client-codegen

Test generator and client library for GraphQL API automated testing.
The generated methods also include logging.

## Установка

Use `pip` to install the package.:

```shell
pip install git+https://github.com/ValeriyMenshikov/graphql-client-codegen.git
```

## Использование

Run command:

```shell
graphql_codegen gen -u http://service_name/graphql/ -s service_name_api -o ./service_name_api -m True
```

A schema, client, and automated tests will be generated. Valid test data will need to be provided in the automated
tests.

Generated client:

```python
from sgqlc.types import ContainerTypeMeta, non_null
from .schema import *
from graphql_codegen.public.base_client.client import GraphQLClient
from graphql_codegen.public.base_client.errors import GraphQLClientError


class GraphQLServiceNameApiClient:
    def __init__(self, host: str, headers: dict = None, disable_log: bool = False):
        self.host = host
        self.headers = headers
        self.disable_log = disable_log
        self.client = GraphQLClient(
            host=self.host,
            schema=schema,
            base_headers=self.headers,
            disable_log=self.disable_log
        )

    @staticmethod
    def _convert_to_model(response: dict, query_name: str, model: ContainerTypeMeta):
        json_data = response.get('data', {}).get(query_name)
        if json_data:
            return model(json_data)
        raise GraphQLClientError(response)

    def account_current(self, access_token: String) -> EnvelopeOfUserDetails | dict:
        query_name = 'accountCurrent'
        query = self.client.query(name=query_name)
        query.account_current(
            access_token=access_token,
        )
        response = self.client.request(query=query)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUserDetails
        )
        return response
```

Conftest file:

```python
import pytest

from ..service_name_api import GraphQLServiceNameApiClient
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def client():
    return GraphQLServiceNameApiClient(host='http://service_name/graphql/')
```

Example of a generated test:

```python
from ..schema import *


class TestsAccountCurrent:

    def test_account_current(self, client):
        # Заполни тестовые данные
        access_token: String = None
        response = client.account_current(
            access_token=access_token,
        )
        assert response
```

Example of a log after running the test:

```sh
graphQL QUERY:
query accountCurrent {
  accountCurrent(accessToken: null) {
    resource {
      icq
      skype
      originalPictureUrl
      login
      roles
      mediumPictureUrl
      smallPictureUrl
      status
      online
      name
      location
      registration
    }
  }
}
{
    "event": "request",
    "headers": {},
    "operation_kind": "query",
    "operation_name": "accountCurrent",
    "request": "query accountCurrent {\n  accountCurrent(accessToken: null) {\n    resource {\n      icq\n      skype\n      originalPictureUrl\n      login\n      roles\n      mediumPictureUrl\n      smallPictureUrl\n      status\n      online\n      name\n      location\n      registration\n    }\n  }\n}",
    "request_id": "0399adde-11b2-4995-9fd3-a3dd2acbcdc8",
    "service": "GraphQL",
    "url": "http://service_name/graphql/"
}
{
    "elapsed_time": "0:00:00.000001",
    "event": "response",
    "request_id": "0399adde-11b2-4995-9fd3-a3dd2acbcdc8",
    "response_data": {
        "data": {
            "accountCurrent": null
        },
        "errors": [
            {
                "locations": [
                    {
                        "column": 1,
                        "line": 2
                    }
                ],
                "message": "Not authorized: ForgedToken",
                "path": [
                    "accountCurrent"
                ]
            }
        ]
    },
    "service": "GraphQL"
}
```

## Documentation

```
Arguments:

-u, --url url address to your service
-o, --output_dir path to generated library
-s, --service_name your api name
-m, --make_tests generate or not tests files (default false)
```

## License

[MIT License](LICENSE)

