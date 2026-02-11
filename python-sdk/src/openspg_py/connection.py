from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class ConnectionInfo:
    scheme: str
    host: str
    port: int
    connect_timeout: float = 6.0
    read_timeout: float = 600.0

    @staticmethod
    def from_uri(
        uri: str, connect_timeout: float = 6.0, read_timeout: float = 600.0
    ) -> "ConnectionInfo":
        parsed = urlparse(uri)
        if not parsed.scheme or not parsed.hostname:
            raise ValueError(f"invalid uri: {uri}")
        if parsed.port is not None:
            port = parsed.port
        elif parsed.scheme == "https":
            port = 443
        else:
            port = 80
        return ConnectionInfo(
            scheme=parsed.scheme,
            host=parsed.hostname,
            port=port,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
        )

    @property
    def base_url(self) -> str:
        return f"{self.scheme}://{self.host}:{self.port}"

