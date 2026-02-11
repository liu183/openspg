from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional


def _strip_none(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}


def _csv(values: Optional[Iterable[Any]]) -> Optional[str]:
    if values is None:
        return None
    normalized = [str(v) for v in values]
    if not normalized:
        return None
    return ",".join(normalized)


class SPGTypeEnum(str, Enum):
    BASIC_TYPE = "BASIC_TYPE"
    ENTITY_TYPE = "ENTITY_TYPE"
    INDEX_TYPE = "INDEX_TYPE"
    CONCEPT_TYPE = "CONCEPT_TYPE"
    EVENT_TYPE = "EVENT_TYPE"
    STANDARD_TYPE = "STANDARD_TYPE"


@dataclass(frozen=True)
class ProjectSchemaRequest:
    project_id: int

    def to_query(self) -> Dict[str, Any]:
        return {"projectId": self.project_id}

    def to_key(self) -> str:
        return str(self.project_id)


@dataclass(frozen=True)
class SPGTypeRequest:
    name: Optional[str] = None
    name_list: Optional[List[str]] = None

    def normalized_name(self) -> str:
        if self.name:
            return self.name
        if self.name_list:
            return ",".join(self.name_list)
        return ""

    def to_query(self) -> Dict[str, Any]:
        return _strip_none({"name": self.normalized_name() or None})

    def to_key(self) -> str:
        return self.normalized_name()


@dataclass(frozen=True)
class RelationRequest:
    s_name: str
    relation: str
    o_name: str

    @staticmethod
    def parse(spg_name: str) -> "RelationRequest":
        splits = spg_name.split("_")
        if len(splits) != 3:
            raise ValueError(f"invalid relation name: {spg_name}")
        return RelationRequest(s_name=splits[0], relation=splits[1], o_name=splits[2])

    def to_query(self) -> Dict[str, Any]:
        return {"sName": self.s_name, "relation": self.relation, "oName": self.o_name}

    def to_key(self) -> str:
        return f"{self.s_name}_{self.relation}_{self.o_name}"


@dataclass(frozen=True)
class BuiltInPropertyRequest:
    spg_type_enum: SPGTypeEnum

    def to_query(self) -> Dict[str, Any]:
        return {"spgTypeEnum": self.spg_type_enum.value}


@dataclass(frozen=True)
class ConceptRequest:
    concept_type_name: str
    concept_name: Optional[str] = None

    def to_query(self) -> Dict[str, Any]:
        return _strip_none(
            {"conceptTypeName": self.concept_type_name, "conceptName": self.concept_name}
        )

    def to_key(self) -> str:
        return f"{self.concept_type_name}/{self.concept_name}"


@dataclass(frozen=True)
class SchemaAlterRequest:
    project_id: int
    schema_draft: Dict[str, Any]

    def to_body(self) -> Dict[str, Any]:
        return {"projectId": self.project_id, "schemaDraft": self.schema_draft}


@dataclass(frozen=True)
class DefineDynamicTaxonomyRequest:
    concept_type_name: str
    concept_name: str
    dsl: str

    def to_body(self) -> Dict[str, Any]:
        return {
            "conceptTypeName": self.concept_type_name,
            "conceptName": self.concept_name,
            "dsl": self.dsl,
        }


@dataclass(frozen=True)
class RemoveDynamicTaxonomyRequest:
    object_concept_type_name: str
    object_concept_name: str

    def to_body(self) -> Dict[str, Any]:
        return {
            "objectConceptTypeName": self.object_concept_type_name,
            "objectConceptName": self.object_concept_name,
        }


@dataclass(frozen=True)
class DefineTripleSemanticRequest:
    subject_concept_type_name: str
    subject_concept_name: str
    predicate_name: str
    object_concept_type_name: str
    object_concept_name: str
    dsl: str
    semantic_type: Optional[str] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "subjectConceptTypeName": self.subject_concept_type_name,
                "subjectConceptName": self.subject_concept_name,
                "predicateName": self.predicate_name,
                "objectConceptTypeName": self.object_concept_type_name,
                "objectConceptName": self.object_concept_name,
                "dsl": self.dsl,
                "semanticType": self.semantic_type,
            }
        )


@dataclass(frozen=True)
class RemoveTripleSemanticRequest:
    subject_concept_type_name: str
    subject_concept_name: str
    predicate_name: str
    object_concept_type_name: str
    object_concept_name: str
    semantic_type: Optional[str] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "subjectConceptTypeName": self.subject_concept_type_name,
                "subjectConceptName": self.subject_concept_name,
                "predicateName": self.predicate_name,
                "objectConceptTypeName": self.object_concept_type_name,
                "objectConceptName": self.object_concept_name,
                "semanticType": self.semantic_type,
            }
        )


@dataclass(frozen=True)
class ProjectCreateRequest:
    name: str
    user_no: str
    namespace: str
    visibility: str
    config: Dict[str, Any]
    tenant_id: Optional[int] = None
    description: Optional[str] = None
    auto_schema: Optional[bool] = None
    tag: Optional[str] = None
    id: Optional[int] = None
    is_knext: Optional[bool] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "namespace": self.namespace,
                "visibility": self.visibility,
                "tenantId": self.tenant_id,
                "config": self.config,
                "autoSchema": self.auto_schema,
                "tag": self.tag,
                "userNo": self.user_no,
                "isKnext": self.is_knext,
            }
        )


@dataclass(frozen=True)
class ProjectUpdateRequest(ProjectCreateRequest):
    id: int


@dataclass(frozen=True)
class ProjectQueryRequest:
    tenant_id: Optional[int] = None
    project_id: Optional[int] = None

    def to_query(self) -> Dict[str, Any]:
        return _strip_none({"tenantId": self.tenant_id, "projectId": self.project_id})


@dataclass(frozen=True)
class TenantCreateRequest:
    name: str
    desc: Optional[str] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none({"name": self.name, "desc": self.desc})


@dataclass(frozen=True)
class TenantQueryRequest:
    tenant_id: Optional[int] = None

    def to_query(self) -> Dict[str, Any]:
        return _strip_none({"tenantId": self.tenant_id})


@dataclass(frozen=True)
class SPGTypeQueryRequest:
    project_id: int
    spg_type: str
    ids: Optional[Iterable[str]] = None

    def to_body(self) -> Dict[str, Any]:
        ids_value = list(self.ids) if self.ids is not None else None
        return _strip_none(
            {"projectId": self.project_id, "spgType": self.spg_type, "ids": ids_value}
        )


@dataclass(frozen=True)
class SPGTypeSearchRequest:
    project_id: int
    keyword: str
    page_size: int = 10
    page_idx: int = 0

    def to_query(self) -> Dict[str, Any]:
        return {
            "projectId": self.project_id,
            "keyword": self.keyword,
            "pageSize": self.page_size,
            "pageIdx": self.page_idx,
        }


@dataclass(frozen=True)
class TextSearchRequest:
    project_id: int
    query_string: str
    label_constraints: Optional[Iterable[str]] = None
    page: Optional[int] = None
    topk: Optional[int] = None

    def to_body(self) -> Dict[str, Any]:
        labels = list(self.label_constraints) if self.label_constraints is not None else None
        return _strip_none(
            {
                "projectId": self.project_id,
                "queryString": self.query_string,
                "labelConstraints": labels,
                "page": self.page,
                "topk": self.topk,
            }
        )


@dataclass(frozen=True)
class VectorSearchRequest:
    project_id: int
    label: str
    property_key: str
    query_vector: List[float]
    ef_search: int
    topk: int

    def to_body(self) -> Dict[str, Any]:
        return {
            "projectId": self.project_id,
            "label": self.label,
            "propertyKey": self.property_key,
            "queryVector": self.query_vector,
            "efSearch": self.ef_search,
            "topk": self.topk,
        }


@dataclass(frozen=True)
class CustomSearchRequest:
    project_id: int
    custom_query: str

    def to_body(self) -> Dict[str, Any]:
        return {"projectId": self.project_id, "customQuery": self.custom_query}


@dataclass(frozen=True)
class ReasonerTaskRequest:
    task_id: str
    project_id: int
    dsl: str
    params: Optional[Dict[str, str]] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "taskId": self.task_id,
                "projectId": self.project_id,
                "dsl": self.dsl,
                "params": self.params,
            }
        )


@dataclass(frozen=True)
class ThinkerTaskRequest:
    project_id: int
    subject: str
    predicate: str
    object: str
    mode: Optional[str] = None
    params: Optional[str] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "projectId": self.project_id,
                "subject": self.subject,
                "predicate": self.predicate,
                "object": self.object,
                "mode": self.mode,
                "params": self.params,
            }
        )


@dataclass(frozen=True)
class GraphLabelRequest:
    project_id: int

    def to_query(self) -> Dict[str, Any]:
        return {"projectId": self.project_id}


@dataclass(frozen=True)
class VertexRecordInstance:
    type: str
    id: str
    properties: Optional[Dict[str, Any]] = None
    vectors: Optional[Dict[str, List[float]]] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "type": self.type,
                "id": self.id,
                "properties": self.properties or {},
                "vectors": self.vectors or {},
            }
        )


@dataclass(frozen=True)
class EdgeRecordInstance:
    src_type: str
    src_id: str
    dst_type: str
    dst_id: str
    label: str
    properties: Optional[Dict[str, Any]] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "srcType": self.src_type,
                "srcId": self.src_id,
                "dstType": self.dst_type,
                "dstId": self.dst_id,
                "label": self.label,
                "properties": self.properties or {},
            }
        )


@dataclass(frozen=True)
class GetPageRankScoresRequest:
    project_id: int
    target_vertex_type: Optional[str] = None
    start_nodes: Optional[List[VertexRecordInstance]] = None

    def to_body(self) -> Dict[str, Any]:
        nodes = None
        if self.start_nodes is not None:
            nodes = [node.to_body() for node in self.start_nodes]
        return _strip_none(
            {
                "projectId": self.project_id,
                "targetVertexType": self.target_vertex_type,
                "startNodes": nodes,
            }
        )


@dataclass(frozen=True)
class UpsertVertexRequest:
    project_id: int
    vertices: List[VertexRecordInstance]

    def to_body(self) -> Dict[str, Any]:
        return {
            "projectId": self.project_id,
            "vertices": [item.to_body() for item in self.vertices],
        }


@dataclass(frozen=True)
class UpsertEdgeRequest:
    project_id: int
    edges: List[EdgeRecordInstance]
    upsert_adjacent_vertices: bool = True

    def to_body(self) -> Dict[str, Any]:
        return {
            "projectId": self.project_id,
            "upsertAdjacentVertices": self.upsert_adjacent_vertices,
            "edges": [item.to_body() for item in self.edges],
        }


@dataclass(frozen=True)
class DeleteVertexRequest:
    project_id: int
    vertices: List[VertexRecordInstance]

    def to_body(self) -> Dict[str, Any]:
        return {
            "projectId": self.project_id,
            "vertices": [item.to_body() for item in self.vertices],
        }


@dataclass(frozen=True)
class DeleteEdgeRequest:
    project_id: int
    edges: List[EdgeRecordInstance]

    def to_body(self) -> Dict[str, Any]:
        return {
            "projectId": self.project_id,
            "edges": [item.to_body() for item in self.edges],
        }


@dataclass(frozen=True)
class WriterGraphRequest:
    sub_graph: Dict[str, Any]
    operation: str
    project_id: int
    enable_lead_to: Optional[bool] = None
    token: Optional[str] = None

    def to_body(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "subGraph": self.sub_graph,
                "operation": self.operation,
                "projectId": self.project_id,
                "enableLeadTo": self.enable_lead_to,
                "token": self.token,
            }
        )


@dataclass(frozen=True)
class SPGTypeSamplingRequest:
    project_id: int
    spg_type: str
    limit: Optional[int] = None

    def to_query(self) -> Dict[str, Any]:
        return _strip_none(
            {"projectId": self.project_id, "spgType": self.spg_type, "limit": self.limit}
        )


@dataclass(frozen=True)
class RelationSamplingRequest:
    project_id: int
    src_spg_type: str
    relation: str
    dst_spg_type: str
    limit: Optional[int] = None

    def to_query(self) -> Dict[str, Any]:
        return _strip_none(
            {
                "projectId": self.project_id,
                "srcSpgType": self.src_spg_type,
                "relation": self.relation,
                "dstSpgType": self.dst_spg_type,
                "limit": self.limit,
            }
        )
