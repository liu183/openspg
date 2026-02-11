from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class ApiException(RuntimeError):
    @staticmethod
    def with_error_msg(error_msg: str) -> "ApiException":
        return ApiException(f"request server with errorMsg: {error_msg}")

    @staticmethod
    def not_found(name: Optional[str]) -> "ApiException":
        normalized = name or ""
        return ApiException(f"{normalized} not found!")

    @staticmethod
    def connect_error(exc: Exception) -> "ApiException":
        _ = exc
        return ApiException("connect server error")


@dataclass
class ApiResponse(Generic[T]):
    data: Optional[T]
    success: bool
    error_msg: Optional[str] = None
    remote: Optional[str] = None
    trace_id: Optional[str] = None

    @staticmethod
    def success_response(
        data: Optional[T], remote: Optional[str] = None, trace_id: Optional[str] = None
    ) -> "ApiResponse[T]":
        return ApiResponse(data=data, success=True, remote=remote, trace_id=trace_id)

    @staticmethod
    def failure_response(
        error_msg: str, remote: Optional[str] = None, trace_id: Optional[str] = None
    ) -> "ApiResponse[T]":
        return ApiResponse(
            data=None,
            success=False,
            error_msg=error_msg,
            remote=remote,
            trace_id=trace_id,
        )

    def unwrap(self) -> Optional[T]:
        if self.success:
            return self.data
        raise ApiException.with_error_msg(self.error_msg or "unknown error")

    def unwrap_not_none(self, name: Optional[str] = None) -> T:
        data = self.unwrap()
        if data is None:
            raise ApiException.not_found(name)
        return data
