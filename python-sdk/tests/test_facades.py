from __future__ import annotations

from openspg_py.api import ApiResponse
from openspg_py.concept import ConceptFacade
from openspg_py.models import (
    ProjectSchemaRequest,
    RelationRequest,
    SPGTypeRequest,
)
from openspg_py.schema import SchemaFacade


class TransportSpy:
    def __init__(self):
        self.calls = []

    def request(self, method, path, *, params=None, json=None):
        self.calls.append(
            {"method": method, "path": path, "params": params or {}, "json": json or {}}
        )
        return ApiResponse.success_response({"ok": True})


def test_schema_cache_hits_for_same_keys():
    transport = TransportSpy()
    schema = SchemaFacade(transport, enable_cache=True, cache_ttl_seconds=1000)

    schema.query_project_schema(ProjectSchemaRequest(project_id=1))
    schema.query_project_schema(ProjectSchemaRequest(project_id=1))
    schema.query_spg_type(SPGTypeRequest(name="Person"))
    schema.query_spg_type(SPGTypeRequest(name="Person"))
    schema.query_relation(RelationRequest("Person", "knows", "Person"))
    schema.query_relation(RelationRequest("Person", "knows", "Person"))

    assert len(transport.calls) == 3


def test_concept_reasoning_query_uses_comma_name():
    transport = TransportSpy()
    concept = ConceptFacade(transport)
    concept.get_reasoning_concepts_detail(SPGTypeRequest(name_list=["A", "B"]))
    assert transport.calls[0]["path"] == "/public/v1/concept/getReasoningConcept"
    assert transport.calls[0]["params"]["name"] == "A,B"

