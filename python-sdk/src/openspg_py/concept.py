from __future__ import annotations

from typing import Any, Dict, List

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import (
    ConceptRequest,
    DefineDynamicTaxonomyRequest,
    DefineTripleSemanticRequest,
    RemoveDynamicTaxonomyRequest,
    RemoveTripleSemanticRequest,
    SPGTypeRequest,
)


class ConceptFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def query_concept(self, request: ConceptRequest) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/concept/queryConcept",
            params=request.to_query(),
        )

    def get_reasoning_concepts_detail(
        self, request: SPGTypeRequest
    ) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "GET",
            "/public/v1/concept/getReasoningConcept",
            params=request.to_query(),
        )

    def define_dynamic_taxonomy(
        self, request: DefineDynamicTaxonomyRequest
    ) -> ApiResponse[bool]:
        return self._transport.request(
            "POST",
            "/public/v1/concept/defineDynamicTaxonomy",
            json=request.to_body(),
        )

    def define_logical_causation(
        self, request: DefineTripleSemanticRequest
    ) -> ApiResponse[bool]:
        return self._transport.request(
            "POST",
            "/public/v1/concept/defineLogicalCausation",
            json=request.to_body(),
        )

    def remove_dynamic_taxonomy(
        self, request: RemoveDynamicTaxonomyRequest
    ) -> ApiResponse[bool]:
        return self._transport.request(
            "POST",
            "/public/v1/concept/removeDynamicTaxonomy",
            json=request.to_body(),
        )

    def remove_logical_causation(
        self, request: RemoveTripleSemanticRequest
    ) -> ApiResponse[bool]:
        return self._transport.request(
            "POST",
            "/public/v1/concept/removeLogicalCausation",
            json=request.to_body(),
        )

