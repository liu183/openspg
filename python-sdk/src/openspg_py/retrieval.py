from __future__ import annotations

from typing import Any, Dict, List, Union

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import RetrievalQueryRequest, RetrievalRequest


def _to_body(payload: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "to_body"):
        return payload.to_body()
    raise TypeError("payload must be dict or model with to_body()")


class RetrievalFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def get_all(self) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request("GET", "/public/v1/retrieval/getAll")

    def delete(self, retrieval_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/retrieval/delete",
            params={"id": retrieval_id},
        )

    def get_by_id(self, retrieval_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/retrieval/getById",
            params={"id": retrieval_id},
        )

    def get_by_project_id(self, project_id: int) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "GET",
            "/public/v1/retrieval/getByProjectId",
            params={"projectId": project_id},
        )

    def search(
        self, payload: Union[Dict[str, Any], RetrievalQueryRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/retrieval/search",
            json=_to_body(payload),
        )

    def update(
        self, payload: Union[Dict[str, Any], RetrievalRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/retrieval/update",
            json=_to_body(payload),
        )
