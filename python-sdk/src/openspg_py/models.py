from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


def _strip_none(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}


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

