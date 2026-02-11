from __future__ import annotations

from typing import Any, Dict

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import KagBuilderRequest


class BuilderFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def kag_submit(self, request: KagBuilderRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/builder/kag/submit",
            json=request.to_body(),
        )

    def delete(self, builder_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/builder/delete",
            params={"id": builder_id},
        )

    def get_by_id(self, builder_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/builder/getById",
            params={"id": builder_id},
        )

    def search(self, payload: Dict[str, Any]) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/builder/search",
            json=payload,
        )

