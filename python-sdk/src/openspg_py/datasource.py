from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import DataSourceQueryRequest, DataSourceRequest


def _to_body(payload: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "to_body"):
        return payload.to_body()
    raise TypeError("payload must be dict or model with to_body()")


class DataSourceFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def insert(
        self, payload: Union[Dict[str, Any], DataSourceRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/datasource/insert",
            json=_to_body(payload),
        )

    def update(
        self, payload: Union[Dict[str, Any], DataSourceRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/datasource/update",
            json=_to_body(payload),
        )

    def delete(self, data_source_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/datasource/delete",
            params={"id": data_source_id},
        )

    def get_by_id(self, data_source_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/datasource/getById",
            params={"id": data_source_id},
        )

    def search(
        self, payload: Union[Dict[str, Any], DataSourceQueryRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/datasource/search",
            json=_to_body(payload),
        )

    def get_all_database(self, data_source_id: int) -> ApiResponse[List[str]]:
        return self._transport.request(
            "GET",
            "/public/v1/datasource/getAllDatabase",
            params={"id": data_source_id},
        )

    def get_all_table(
        self, data_source_id: int, db_name: str, keyword: Optional[str] = None
    ) -> ApiResponse[List[str]]:
        params = {"id": data_source_id, "dbName": db_name}
        if keyword is not None:
            params["keyword"] = keyword
        return self._transport.request(
            "GET",
            "/public/v1/datasource/getAllTable",
            params=params,
        )

    def get_table_detail(
        self, data_source_id: int, db_name: str, table_name: str
    ) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "GET",
            "/public/v1/datasource/getTableDetail",
            params={"id": data_source_id, "dbName": db_name, "tableName": table_name},
        )

    def test_connect(
        self, payload: Union[Dict[str, Any], DataSourceRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/datasource/testConnect",
            json=_to_body(payload),
        )

    def get_data_source_type(
        self, category: Optional[str] = None
    ) -> ApiResponse[List[Dict[str, Any]]]:
        params: Dict[str, Any] = {}
        if category is not None:
            params["category"] = category
        return self._transport.request(
            "GET",
            "/public/v1/datasource/getDataSourceType",
            params=params,
        )

    def get_data_source_group_by_type(
        self, payload: Union[Dict[str, Any], DataSourceQueryRequest]
    ) -> ApiResponse[List[Dict[str, Any]]]:
        return self._transport.request(
            "POST",
            "/public/v1/datasource/getDataSourceGroupByType",
            json=_to_body(payload),
        )
