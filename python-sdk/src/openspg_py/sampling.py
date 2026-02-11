from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import RelationSamplingRequest, SPGTypeSamplingRequest


class SamplingFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def spg_type(self, request: SPGTypeSamplingRequest) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "GET",
            "/public/v1/sampling/spgType",
            params=request.to_query(),
        )

    def relation(self, request: RelationSamplingRequest) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "GET",
            "/public/v1/sampling/relation",
            params=request.to_query(),
        )

