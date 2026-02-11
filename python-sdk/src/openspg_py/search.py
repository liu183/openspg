from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import (
    CustomSearchRequest,
    SPGTypeSearchRequest,
    TextSearchRequest,
    VectorSearchRequest,
)


class SearchFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def spg_type(self, request: SPGTypeSearchRequest) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "GET",
            "/public/v1/search/spgType",
            params=request.to_query(),
        )

    def text(self, request: TextSearchRequest) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "POST",
            "/public/v1/search/text",
            json=request.to_body(),
        )

    def vector(self, request: VectorSearchRequest) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "POST",
            "/public/v1/search/vector",
            json=request.to_body(),
        )

    def custom(self, request: CustomSearchRequest) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "POST",
            "/public/v1/search/custom",
            json=request.to_body(),
        )

