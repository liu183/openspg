from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import ConceptInstanceQueryRequest, ConceptLevelInstanceRequest


class ConceptInstanceFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def level(
        self, request: ConceptLevelInstanceRequest
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/conceptInstance/level",
            params=request.to_query(),
        )

    def query(
        self, request: ConceptInstanceQueryRequest
    ) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "GET",
            "/public/v1/conceptInstance",
            params=request.to_query(),
        )

