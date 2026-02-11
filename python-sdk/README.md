# OpenSPG Python SDK (Migration)

This directory is a Python engineering conversion of key OpenSPG Java client capability.

Current migration scope:

- Converted Java module: `server/api/http-client`
- Converted facades:
  - `HttpSchemaFacade` -> `SchemaFacade`
  - `HttpConceptFacade` -> `ConceptFacade`
- Additional openapi facades:
  - `ProjectFacade`, `TenantFacade`
  - `QueryFacade`, `ReasonFacade`
  - `SearchFacade`, `GraphFacade`, `SamplingFacade`
  - `ConceptInstanceFacade`
  - `DataSourceFacade`, `RetrievalFacade`
  - `SearchEngineFacade`, `BuilderFacade`
- Converted support classes:
  - `ConnectionInfo`
  - `ApiResponse`
  - `ApiException`
  - request DTOs used by schema/concept APIs
- Preserved Java client semantics:
  - non-2xx response -> `ApiResponse.success=False`
  - `404` -> `ApiResponse.success=True, data=None`
  - connection failure -> raise `ApiException.connect_error`

## Install

```bash
pip install -e .[dev]
```

## Quick Start

```python
from openspg_py import OpenSPGClient, ProjectSchemaRequest

client = OpenSPGClient("http://127.0.0.1:8887", enable_schema_cache=True)
resp = client.schema.query_project_schema(ProjectSchemaRequest(project_id=1))

schema = resp.unwrap_not_none("project schema")
print(schema)
```

## Example: Query Concept

```python
from openspg_py import OpenSPGClient, ConceptRequest

client = OpenSPGClient("http://127.0.0.1:8887")
resp = client.concept.query_concept(
    ConceptRequest(concept_type_name="RiskConcept")
)
print(resp.unwrap())
```

## Example: Search and Graph

```python
from openspg_py import (
    OpenSPGClient,
    SPGTypeSearchRequest,
    GraphLabelRequest,
)

client = OpenSPGClient("http://127.0.0.1:8887")
search_resp = client.search.spg_type(
    SPGTypeSearchRequest(project_id=1, keyword="Person")
)
print(search_resp.unwrap())

labels_resp = client.graph.all_labels(GraphLabelRequest(project_id=1))
print(labels_resp.unwrap())
```

## Run tests

```bash
pytest
```
