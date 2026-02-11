from __future__ import annotations

from typing import Optional

import requests

from ._http import OpenSPGHttpTransport
from .concept import ConceptFacade
from .connection import ConnectionInfo
from .graph import GraphFacade
from .project import ProjectFacade
from .query import QueryFacade
from .reason import ReasonFacade
from .sampling import SamplingFacade
from .schema import SchemaFacade
from .search import SearchFacade
from .tenant import TenantFacade


class OpenSPGClient:
    def __init__(
        self,
        uri: str,
        *,
        connect_timeout: float = 6.0,
        read_timeout: float = 600.0,
        token: Optional[str] = None,
        enable_schema_cache: bool = False,
        session: Optional[requests.Session] = None,
    ) -> None:
        connection = ConnectionInfo.from_uri(
            uri,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
        )
        transport = OpenSPGHttpTransport(
            connection_info=connection,
            token=token,
            session=session,
        )
        self.schema = SchemaFacade(transport, enable_cache=enable_schema_cache)
        self.concept = ConceptFacade(transport)
        self.project = ProjectFacade(transport)
        self.tenant = TenantFacade(transport)
        self.query = QueryFacade(transport)
        self.reason = ReasonFacade(transport)
        self.search = SearchFacade(transport)
        self.graph = GraphFacade(transport)
        self.sampling = SamplingFacade(transport)
