import pprint
import uuid
from datetime import datetime
from typing import Any, Dict
import structlog
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from sgqlc.types import Schema


class GraphQLClient:

    def __init__(
            self,
            schema: Schema,
            host: str,
            disable_log: bool = False,
            base_headers: dict = None
    ):
        self.schema = schema
        self.disable_log = disable_log
        self.host = host
        self._endpoint = HTTPEndpoint(self.host)
        self.log = structlog.get_logger(__name__).bind(service="GraphQL")

        if base_headers:
            self._endpoint.base_headers = base_headers

    def set_headers(self, headers: dict) -> None:
        self._endpoint.base_headers = headers

    def query(self, name: str) -> Operation:
        return Operation(self.schema.Query, name)

    def mutation(self, name: str) -> Operation:
        return Operation(self.schema.Mutation, name)

    def request(self, query: Operation) -> Dict[str, Any]:

        if self.disable_log:
            return self._endpoint(query=query)

        start_time = datetime.now()
        end_time = datetime.now()
        elapsed_time = str(end_time - start_time)
        print('\ngraphQL QUERY:')
        pprint.pp(query)
        log = self.log.bind(request_id=str(uuid.uuid4()))
        log.msg(
            "request",
            url=self._endpoint.url,
            headers=self._endpoint.base_headers,
            operation_kind=query._Operation__kind,
            operation_name=query._Operation__name,
            request=query,
        )
        response = self._endpoint(query=query)

        log.msg(
            "response",
            response_data=response,
            elapsed_time=elapsed_time
        )
        return response
