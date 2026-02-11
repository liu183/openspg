from __future__ import annotations

from openspg_py.api import ApiResponse
from openspg_py.graph import GraphFacade
from openspg_py.models import (
    CustomSearchRequest,
    EdgeRecordInstance,
    GraphLabelRequest,
    ProjectCreateRequest,
    ProjectQueryRequest,
    ReasonerTaskRequest,
    RelationSamplingRequest,
    SPGTypeQueryRequest,
    SPGTypeSamplingRequest,
    SPGTypeSearchRequest,
    TenantCreateRequest,
    TenantQueryRequest,
    TextSearchRequest,
    ThinkerTaskRequest,
    UpsertEdgeRequest,
    UpsertVertexRequest,
    VectorSearchRequest,
    VertexRecordInstance,
)
from openspg_py.project import ProjectFacade
from openspg_py.query import QueryFacade
from openspg_py.reason import ReasonFacade
from openspg_py.sampling import SamplingFacade
from openspg_py.search import SearchFacade
from openspg_py.tenant import TenantFacade


class TransportSpy:
    def __init__(self):
        self.calls = []

    def request(self, method, path, *, params=None, json=None):
        self.calls.append(
            {"method": method, "path": path, "params": params or {}, "json": json or {}}
        )
        return ApiResponse.success_response({"ok": True})


def test_project_tenant_facades():
    t = TransportSpy()
    project = ProjectFacade(t)
    tenant = TenantFacade(t)

    project.create(
        ProjectCreateRequest(
            name="demo",
            user_no="owner_001",
            namespace="demo_ns",
            visibility="PRIVATE",
            config={"vectorizer": "x"},
            tag="LOCAL",
        )
    )
    project.query(ProjectQueryRequest(tenant_id=2, project_id=3))
    tenant.create(TenantCreateRequest(name="t1", desc="d"))
    tenant.query(TenantQueryRequest(tenant_id=7))

    assert t.calls[0]["path"] == "/public/v1/project"
    assert t.calls[0]["json"]["name"] == "demo"
    assert t.calls[1]["params"]["tenantId"] == 2
    assert t.calls[1]["params"]["projectId"] == 3
    assert t.calls[2]["path"] == "/public/v1/tenant"
    assert t.calls[3]["params"]["tenantId"] == 7


def test_query_reason_search_sampling_facades():
    t = TransportSpy()
    query = QueryFacade(t)
    reason = ReasonFacade(t)
    search = SearchFacade(t)
    sampling = SamplingFacade(t)

    query.query_spg_type(SPGTypeQueryRequest(project_id=1, spg_type="Person", ids={"1", "2"}))
    reason.run(ReasonerTaskRequest(task_id="r1", project_id=1, dsl="MATCH", params={"k": "v"}))
    reason.thinker(
        ThinkerTaskRequest(project_id=1, subject="A", predicate="p", object="B", mode="default")
    )
    reason.schema(1)
    search.spg_type(SPGTypeSearchRequest(project_id=1, keyword="Person"))
    search.text(TextSearchRequest(project_id=1, query_string="hello", label_constraints={"A"}))
    search.vector(
        VectorSearchRequest(
            project_id=1,
            label="Person",
            property_key="embedding",
            query_vector=[0.1, 0.2],
            ef_search=100,
            topk=10,
        )
    )
    search.custom(CustomSearchRequest(project_id=1, custom_query="query"))
    sampling.spg_type(SPGTypeSamplingRequest(project_id=1, spg_type="Person", limit=5))
    sampling.relation(
        RelationSamplingRequest(
            project_id=1, src_spg_type="A", relation="r", dst_spg_type="B", limit=3
        )
    )

    assert t.calls[0]["path"] == "/public/v1/query/spgType"
    assert t.calls[1]["path"] == "/public/v1/reason/run"
    assert t.calls[3]["params"]["projectId"] == 1
    assert t.calls[4]["path"] == "/public/v1/search/spgType"
    assert t.calls[8]["path"] == "/public/v1/sampling/spgType"
    assert t.calls[9]["params"]["relation"] == "r"


def test_graph_facade():
    t = TransportSpy()
    graph = GraphFacade(t)

    vertices = [VertexRecordInstance(type="Person", id="u1")]
    edges = [EdgeRecordInstance(src_type="Person", src_id="u1", dst_type="Person", dst_id="u2", label="knows")]

    graph.all_labels(GraphLabelRequest(project_id=1))
    graph.upsert_vertex(UpsertVertexRequest(project_id=1, vertices=vertices))
    graph.upsert_edge(UpsertEdgeRequest(project_id=1, edges=edges))

    assert t.calls[0]["path"] == "/public/v1/graph/allLabels"
    assert t.calls[0]["params"]["projectId"] == 1
    assert t.calls[1]["json"]["vertices"][0]["type"] == "Person"
    assert t.calls[2]["json"]["edges"][0]["label"] == "knows"

