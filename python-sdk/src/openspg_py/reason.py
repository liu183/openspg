from __future__ import annotations

from typing import Any, Dict

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import ReasonerTaskRequest, ThinkerTaskRequest


class ReasonFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def run(self, request: ReasonerTaskRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/reason/run",
            json=request.to_body(),
        )

    def thinker(self, request: ThinkerTaskRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/reason/thinker",
            json=request.to_body(),
        )

    def schema(self, project_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/reason/schema",
            params={"projectId": project_id},
        )

