from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse


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

    def search(self, payload: Dict[str, Any]) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/retrieval/search",
            json=payload,
        )

    def update(self, payload: Dict[str, Any]) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/retrieval/update",
            json=payload,
        )

