from __future__ import annotations

from openspg_py.api import ApiResponse
from openspg_py.builder import BuilderFacade
from openspg_py.concept_instance import ConceptInstanceFacade
from openspg_py.datasource import DataSourceFacade
from openspg_py.models import (
    ConceptInstanceQueryRequest,
    ConceptLevelInstanceRequest,
    KagBuilderRequest,
    SearchEngineIndexRequest,
)
from openspg_py.retrieval import RetrievalFacade
from openspg_py.scheduler import SchedulerFacade
from openspg_py.search_engine import SearchEngineFacade


class TransportSpy:
    def __init__(self):
        self.calls = []

    def request(self, method, path, *, params=None, json=None):
        self.calls.append(
            {"method": method, "path": path, "params": params or {}, "json": json or {}}
        )
        return ApiResponse.success_response({"ok": True})


def test_concept_instance_facade():
    t = TransportSpy()
    facade = ConceptInstanceFacade(t)
    facade.level(ConceptLevelInstanceRequest(project_id=1, concept_type="RiskConcept"))
    facade.query(
        ConceptInstanceQueryRequest(
            project_id=1, concept_type="RiskConcept", concept_instance_ids={"c1", "c2"}
        )
    )

    assert t.calls[0]["path"] == "/public/v1/conceptInstance/level"
    assert t.calls[0]["params"]["conceptType"] == "RiskConcept"
    assert t.calls[1]["path"] == "/public/v1/conceptInstance"
    assert "conceptInstanceIds" in t.calls[1]["params"]


def test_data_source_and_retrieval_facades():
    t = TransportSpy()
    data_source = DataSourceFacade(t)
    retrieval = RetrievalFacade(t)

    data_source.insert({"dbName": "db1", "dbUrl": "jdbc://x"})
    data_source.get_all_table(10, "db1", keyword="user")
    data_source.get_table_detail(10, "db1", "orders")
    data_source.get_data_source_type("MYSQL")
    retrieval.get_all()
    retrieval.get_by_project_id(8)
    retrieval.search({"projectId": 8, "keyword": "ret"})

    assert t.calls[0]["path"] == "/public/v1/datasource/insert"
    assert t.calls[1]["params"]["dbName"] == "db1"
    assert t.calls[2]["params"]["tableName"] == "orders"
    assert t.calls[4]["path"] == "/public/v1/retrieval/getAll"
    assert t.calls[5]["params"]["projectId"] == 8


def test_search_engine_and_builder_facades():
    t = TransportSpy()
    search_engine = SearchEngineFacade(t)
    builder = BuilderFacade(t)

    search_engine.index(SearchEngineIndexRequest(spg_type="Person"))
    builder.kag_submit(
        KagBuilderRequest(project_id=1, command="python run.py", worker_num=2, user_number="u001")
    )
    builder.search({"projectId": 1, "pageNo": 1, "pageSize": 10})

    assert t.calls[0]["path"] == "/public/v1/searchEngine/index"
    assert t.calls[0]["params"]["spgType"] == "Person"
    assert t.calls[1]["path"] == "/public/v1/builder/kag/submit"
    assert t.calls[1]["json"]["workerNum"] == 2
    assert t.calls[2]["path"] == "/public/v1/builder/search"


def test_scheduler_facade():
    t = TransportSpy()
    scheduler = SchedulerFacade(t)

    scheduler.submit_job({"projectId": 1, "name": "job1"})
    scheduler.execute_job(10)
    scheduler.enable_job(10)
    scheduler.disable_job(10)
    scheduler.delete_job(10)
    scheduler.update_job({"id": 10, "projectId": 1, "name": "job1-updated"})
    scheduler.get_job_by_id(10)
    scheduler.search_jobs({"projectId": 1, "pageNo": 1, "pageSize": 10})
    scheduler.get_instance_by_id(20)
    scheduler.stop_instance(20)
    scheduler.set_finish_instance(20)
    scheduler.restart_instance(20)
    scheduler.trigger_instance(20)
    scheduler.search_instances({"jobId": 10})
    scheduler.search_tasks({"instanceId": 20})
    scheduler.set_ip("127.0.0.1")

    assert t.calls[0]["path"] == "/public/v1/scheduler/job/submit"
    assert t.calls[1]["path"] == "/public/v1/scheduler/job/execute"
    assert t.calls[7]["path"] == "/public/v1/scheduler/job/search"
    assert t.calls[8]["path"] == "/public/v1/scheduler/instance/getById"
    assert t.calls[15]["path"] == "/public/v1/scheduler/setIp"
