# OpenSPG Project Analysis (from `openspg_src`)

## 1. Repository profile

- Branch: `master`
- Latest commit (local clone): `ceeb3ef` (`fix(all): version 0.8 (#572)`)
- Build system: Maven multi-module (`pom.xml` at root)
- Main languages:
  - Java: 1384 files
  - Scala: 167 files
  - XML (Maven + configs): 88 files

Top-level modules from root `pom.xml`:

- `common/util`
- `server`
- `reasoner`
- `builder`
- `cloudext`

## 2. High-level architecture mapping

- `server`: API layer, schema management, services, and HTTP controllers
- `reasoner`: rule engine / KGDSL / logical reasoning components
- `builder`: data-to-graph build pipelines and local runner
- `cloudext`: pluggable storage/search/cache/object-storage/computing adapters
- `common`: shared utilities and base components

## 3. Why this migration boundary first

A full Java/Scala -> Python rewrite is large and multi-quarter work.  
The most reusable boundary for Python consumers is the HTTP client contract already present in Java:

- Java source migrated:
  - `server/api/http-client/src/main/java/.../HttpSchemaFacade.java`
  - `server/api/http-client/src/main/java/.../HttpConceptFacade.java`
  - `server/api/http-client/src/main/java/.../util/ConnectionInfo.java`
  - `server/api/facade/src/main/java/.../ApiResponse.java`
  - related request DTOs under `server/api/facade/.../dto/schema/request`
  - semantic request DTOs under `server/core/schema/model/.../semantic/request`

This gives Python programs immediate interoperability with OpenSPG server APIs.

## 4. Resulting Python project

- Path: `openspg_src/python-sdk`
- Package: `openspg_py`
- Coverage:
  - schema APIs under `/public/v1/schema/*`
  - concept APIs under `/public/v1/concept/*`
  - response and error semantics aligned with Java client
  - optional schema TTL cache aligned with Java cache intent

## 5. Remaining migration backlog (not converted yet)

- Full server-side implementation (`server/biz`, `server/core`, `server/infra`)
- builder execution engine and pipeline runtime
- reasoner internals and KGDSL execution stack
- cloudext provider implementations (Neo4j, TuGraph, Redis, Elasticsearch, etc.)

