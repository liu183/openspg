from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import SPGTypeQueryRequest


class QueryFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def query_spg_type(
        self, request: SPGTypeQueryRequest
    ) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "POST",
            "/public/v1/query/spgType",
            json=request.to_body(),
        )

