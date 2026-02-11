from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import ProjectCreateRequest, ProjectQueryRequest, ProjectUpdateRequest


class ProjectFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def create(self, request: ProjectCreateRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request("POST", "/public/v1/project", json=request.to_body())

    def query(self, request: ProjectQueryRequest) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request("GET", "/public/v1/project", params=request.to_query())

    def update(self, request: ProjectUpdateRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST", "/public/v1/project/update", json=request.to_body()
        )

