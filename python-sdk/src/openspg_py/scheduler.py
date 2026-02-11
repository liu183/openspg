from __future__ import annotations

from typing import Any, Dict, Union

from ._http import OpenSPGHttpTransport
from .api import ApiResponse
from .models import (
    SchedulerInstanceQueryRequest,
    SchedulerJobQueryRequest,
    SchedulerJobRequest,
    SchedulerTaskQueryRequest,
)


def _to_body(payload: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "to_body"):
        return payload.to_body()
    raise TypeError("payload must be dict or model with to_body()")


class SchedulerFacade:
    def __init__(self, transport: OpenSPGHttpTransport) -> None:
        self._transport = transport

    def submit_job(
        self, payload: Union[Dict[str, Any], SchedulerJobRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/scheduler/job/submit",
            json=_to_body(payload),
        )

    def execute_job(self, job_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/job/execute",
            params={"id": job_id},
        )

    def enable_job(self, job_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/job/enable",
            params={"id": job_id},
        )

    def disable_job(self, job_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/job/disable",
            params={"id": job_id},
        )

    def delete_job(self, job_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/job/delete",
            params={"id": job_id},
        )

    def update_job(
        self, payload: Union[Dict[str, Any], SchedulerJobRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/scheduler/job/update",
            json=_to_body(payload),
        )

    def get_job_by_id(self, job_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/job/getById",
            params={"id": job_id},
        )

    def search_jobs(
        self, payload: Union[Dict[str, Any], SchedulerJobQueryRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/scheduler/job/search",
            json=_to_body(payload),
        )

    def get_instance_by_id(self, instance_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/instance/getById",
            params={"id": instance_id},
        )

    def stop_instance(self, instance_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/instance/stop",
            params={"id": instance_id},
        )

    def set_finish_instance(self, instance_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/instance/setFinish",
            params={"id": instance_id},
        )

    def restart_instance(self, instance_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/instance/restart",
            params={"id": instance_id},
        )

    def trigger_instance(self, instance_id: int) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/instance/trigger",
            params={"id": instance_id},
        )

    def search_instances(
        self, payload: Union[Dict[str, Any], SchedulerInstanceQueryRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/scheduler/instance/search",
            json=_to_body(payload),
        )

    def search_tasks(
        self, payload: Union[Dict[str, Any], SchedulerTaskQueryRequest]
    ) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "POST",
            "/public/v1/scheduler/task/search",
            json=_to_body(payload),
        )

    def set_ip(self, ip: str) -> ApiResponse[Dict[str, Any]]:
        return self._transport.request(
            "GET",
            "/public/v1/scheduler/setIp",
            params={"ip": ip},
        )
