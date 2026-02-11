from __future__ import annotations

from typing import Any, Dict

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import SearchEngineIndexRequest


class SearchEngineFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def index(self, request: SearchEngineIndexRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/searchEngine/index",
            params=request.to_query(),
        )

