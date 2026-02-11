from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import TenantCreateRequest, TenantQueryRequest


class TenantFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def create(self, request: TenantCreateRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request("POST", "/public/v1/tenant", json=request.to_body())

    def query(self, request: TenantQueryRequest) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request("GET", "/public/v1/tenant", params=request.to_query())

