from __future__ import annotations

from typing import Any, Dict, List

from cachetools import TTLCache

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import (
    BuiltInPropertyRequest,
    ProjectSchemaRequest,
    RelationRequest,
    SPGTypeRequest,
    SchemaAlterRequest,
)


class SchemaFacade:
    def __init__(
        self,
        transport: OpenSPGHttpTransport,
        *,
        enable_cache: bool = False,
        cache_ttl_seconds: int = 180,
    ) -> None:
        self._transport = transport
        self._project_schema_cache: TTLCache[str, ApiResponse[Dict[str, Any]]] | None = None
        self._spg_type_cache: TTLCache[str, ApiResponse[Dict[str, Any]]] | None = None
        self._relation_cache: TTLCache[str, ApiResponse[Dict[str, Any]]] | None = None
        if enable_cache:
            self._project_schema_cache = TTLCache(maxsize=50, ttl=cache_ttl_seconds)
            self._spg_type_cache = TTLCache(maxsize=1000, ttl=cache_ttl_seconds)
            self._relation_cache = TTLCache(maxsize=1000, ttl=cache_ttl_seconds)

    def alter_schema(self, request: SchemaAlterRequest) -> ApiResponse[bool]:
        return self._transport.request(
            "POST",
            "/public/v1/schema/alterSchema",
            json=request.to_body(),
        )

    def query_project_schema(
        self, request: ProjectSchemaRequest
    ) -> ApiResponse[Dict[str, Any]]:
        if self._project_schema_cache is not None:
            key = request.to_key()
            if key in self._project_schema_cache:
                return self._project_schema_cache[key]
            value = self._transport.request(
                "GET",
                "/public/v1/schema/queryProjectSchema",
                params=request.to_query(),
            )
            self._project_schema_cache[key] = value
            return value
        return self._transport.request(
            "GET",
            "/public/v1/schema/queryProjectSchema",
            params=request.to_query(),
        )

    def query_spg_type(self, request: SPGTypeRequest) -> ApiResponse[Dict[str, Any]]:
        if self._spg_type_cache is not None:
            key = request.to_key()
            if key in self._spg_type_cache:
                return self._spg_type_cache[key]
            value = self._transport.request(
                "GET",
                "/public/v1/schema/querySpgType",
                params=request.to_query(),
            )
            self._spg_type_cache[key] = value
            return value
        return self._transport.request(
            "GET",
            "/public/v1/schema/querySpgType",
            params=request.to_query(),
        )

    def query_relation(self, request: RelationRequest) -> ApiResponse[Dict[str, Any]]:
        if self._relation_cache is not None:
            key = request.to_key()
            if key in self._relation_cache:
                return self._relation_cache[key]
            value = self._transport.request(
                "GET",
                "/public/v1/schema/queryRelation",
                params=request.to_query(),
            )
            self._relation_cache[key] = value
            return value
        return self._transport.request(
            "GET",
            "/public/v1/schema/queryRelation",
            params=request.to_query(),
        )

    def query_built_in_property(
        self, request: BuiltInPropertyRequest
    ) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "GET",
            "/public/v1/schema/queryBuiltInProperty",
            params=request.to_query(),
        )

