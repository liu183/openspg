from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from .api import ApiException, ApiResponse
from .connection import ConnectionInfo

TRACE_ID_HEADER = "TraceId"
REMOTE_HEADER = "Remote"
TOKEN_HEADER = "token"


class OpenSPGHttpTransport:
    def __init__(
        self,
        connection_info: ConnectionInfo,
        token: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._connection_info = connection_info
        self._token = token
        self._session = session or requests.Session()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> ApiResponse[Any]:
        url = f"{self._connection_info.base_url}{path}"
        headers: Dict[str, str] = {}
        if self._token:
            headers[TOKEN_HEADER] = self._token

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=headers,
                timeout=(
                    self._connection_info.connect_timeout,
                    self._connection_info.read_timeout,
                ),
            )
        except requests.RequestException as exc:
            raise ApiException.connect_error(exc) from exc

        remote = response.headers.get(REMOTE_HEADER)
        trace_id = response.headers.get(TRACE_ID_HEADER)
        if response.status_code == 404:
            return ApiResponse.success_response(None, remote=remote, trace_id=trace_id)

        if 200 <= response.status_code < 300:
            if response.content:
                data = response.json()
            else:
                data = None
            return ApiResponse.success_response(data, remote=remote, trace_id=trace_id)

        return ApiResponse.failure_response(
            response.text or f"HTTP {response.status_code}",
            remote=remote,
            trace_id=trace_id,
        )

