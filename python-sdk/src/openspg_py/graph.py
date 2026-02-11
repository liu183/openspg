from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import (
    DeleteEdgeRequest,
    DeleteVertexRequest,
    GetPageRankScoresRequest,
    GraphLabelRequest,
    UpsertEdgeRequest,
    UpsertVertexRequest,
    WriterGraphRequest,
)


class GraphFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def all_labels(self, request: GraphLabelRequest) -> ApiResponse[List[str]]:
        return self._transport.request(
            "GET",
            "/public/v1/graph/allLabels",
            params=request.to_query(),
        )

    def get_page_rank_scores(
        self, request: GetPageRankScoresRequest
    ) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "POST",
            "/public/v1/graph/getPageRankScores",
            json=request.to_body(),
        )

    def upsert_vertex(self, request: UpsertVertexRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/graph/upsertVertex",
            json=request.to_body(),
        )

    def upsert_edge(self, request: UpsertEdgeRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/graph/upsertEdge",
            json=request.to_body(),
        )

    def delete_vertex(self, request: DeleteVertexRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/graph/deleteVertex",
            json=request.to_body(),
        )

    def delete_edge(self, request: DeleteEdgeRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/graph/deleteEdge",
            json=request.to_body(),
        )

    def writer_graph(self, request: WriterGraphRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/graph/writerGraph",
            json=request.to_body(),
        )

