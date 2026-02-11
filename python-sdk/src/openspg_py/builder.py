from __future__ import annotations

from typing import Any, Dict, Union

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import BuilderJobQueryRequest, KagBuilderRequest


def _to_body(payload: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "to_body"):
        return payload.to_body()
    raise TypeError("payload must be dict or model with to_body()")


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

    def search(
        self, payload: Union[Dict[str, Any], BuilderJobQueryRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/builder/search",
            json=_to_body(payload),
        )
