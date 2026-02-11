from __future__ import annotations

import json

import pytest
import requests

from openspg_py._http import OpenSPGHttpTransport
from openspg_py.api import ApiException
from openspg_py.connection import ConnectionInfo


def make_response(
    status_code: int,
    body: object,
    *,
    headers: dict[str, str] | None = None,
) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response.headers.update(headers or {})
    if isinstance(body, (dict, list)):
        response._content = json.dumps(body).encode("utf-8")
        response.headers["Content-Type"] = "application/json"
    elif body is None:
        response._content = b""
    else:
        response._content = str(body).encode("utf-8")
    response.encoding = "utf-8"
    return response


class SessionStub:
    def __init__(self, response: requests.Response | None = None, error: Exception | None = None):
        self._response = response
        self._error = error
        self.last_kwargs = None

    def request(self, **kwargs):
        self.last_kwargs = kwargs
        if self._error:
            raise self._error
        return self._response


def test_transport_success_json():
    session = SessionStub(
        response=make_response(
            200,
            {"value": 1},
            headers={"TraceId": "t1", "Remote": "10.0.0.1"},
        )
    )
    transport = OpenSPGHttpTransport(
        ConnectionInfo.from_uri("http://127.0.0.1:8887"), session=session
    )
    result = transport.request("GET", "/public/v1/schema/querySpgType", params={"name": "A"})
    assert result.success is True
    assert result.data == {"value": 1}
    assert result.trace_id == "t1"
    assert result.remote == "10.0.0.1"


def test_transport_404_returns_success_none():
    session = SessionStub(response=make_response(404, None))
    transport = OpenSPGHttpTransport(
        ConnectionInfo.from_uri("http://127.0.0.1:8887"), session=session
    )
    result = transport.request("GET", "/public/v1/schema/querySpgType", params={"name": "A"})
    assert result.success is True
    assert result.data is None


def test_transport_failure_response():
    session = SessionStub(response=make_response(400, "bad request"))
    transport = OpenSPGHttpTransport(
        ConnectionInfo.from_uri("http://127.0.0.1:8887"), session=session
    )
    result = transport.request("GET", "/public/v1/schema/querySpgType", params={"name": "A"})
    assert result.success is False
    assert "bad request" in (result.error_msg or "")


def test_transport_connection_error_raises():
    session = SessionStub(error=requests.ConnectionError("connect fail"))
    transport = OpenSPGHttpTransport(
        ConnectionInfo.from_uri("http://127.0.0.1:8887"), session=session
    )
    with pytest.raises(ApiException):
        transport.request("GET", "/public/v1/schema/querySpgType", params={"name": "A"})

