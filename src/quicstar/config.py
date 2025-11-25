from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


DEFAULT_HOST = "::1"
DEFAULT_PORT = 8000
DEFAULT_APP = "quicstar.server:default_app"


@dataclass
class QuicstarConfig:
    """Konfiguration für den Quicstar-Server.

    Die Konfiguration kann aus einer TOML-Datei, über Umgebungsvariablen
    oder direkt per CLI gesetzt werden. Für Framework-Integrationen (z. B.
    Django) sollte die jeweilige native Konfiguration verwendet werden, der
    Server nutzt dann lediglich den ASGI-Pfad.
    """

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    app: str = DEFAULT_APP
    protocol_mode: str = "auto"  # auto|http3|http1
    workers: int = field(default_factory=os.cpu_count)
    access_log: bool = True
    log_level: str = "info"
    certfile: Optional[Path] = None
    keyfile: Optional[Path] = None
    quic_bind: Optional[str] = None

    @classmethod
    def from_toml(cls, path: Path) -> "QuicstarConfig":
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        server_data = data.get("server", {})
        return cls(**cls._normalize(server_data))

    @classmethod
    def from_env(cls) -> "QuicstarConfig":
        return cls(
            host=os.getenv("QUICSTAR_HOST", DEFAULT_HOST),
            port=int(os.getenv("QUICSTAR_PORT", DEFAULT_PORT)),
            app=os.getenv("QUICSTAR_APP", DEFAULT_APP),
            protocol_mode=os.getenv("QUICSTAR_PROTOCOL", "auto"),
            workers=int(os.getenv("QUICSTAR_WORKERS", os.cpu_count() or 1)),
            access_log=os.getenv("QUICSTAR_ACCESS_LOG", "true").lower() == "true",
            log_level=os.getenv("QUICSTAR_LOG_LEVEL", "info"),
            certfile=cls._maybe_path(os.getenv("QUICSTAR_CERTFILE")),
            keyfile=cls._maybe_path(os.getenv("QUICSTAR_KEYFILE")),
            quic_bind=os.getenv("QUICSTAR_QUIC_BIND"),
        )

    @classmethod
    def merge(cls, base: "QuicstarConfig", override: "QuicstarConfig") -> "QuicstarConfig":
        data = {**base.__dict__, **{k: v for k, v in override.__dict__.items() if v is not None}}
        return cls(**data)

    @staticmethod
    def _maybe_path(value: Optional[str]) -> Optional[Path]:
        return Path(value) if value else None

    @staticmethod
    def _normalize(raw: dict) -> dict:
        normalized = dict(raw)
        if "certfile" in normalized and normalized["certfile"]:
            normalized["certfile"] = Path(normalized["certfile"])
        if "keyfile" in normalized and normalized["keyfile"]:
            normalized["keyfile"] = Path(normalized["keyfile"])
        return normalized

    def ensure_valid(self) -> None:
        valid_modes = {"auto", "http3", "http1"}
        if self.protocol_mode not in valid_modes:
            raise ValueError(f"protocol_mode muss eine dieser Optionen sein: {', '.join(valid_modes)}")
        if self.protocol_mode == "http3" and not self.certfile:
            raise ValueError("Für HTTP/3 muss ein TLS-Zertifikat (certfile) angegeben werden.")
        if self.keyfile and not self.certfile:
            raise ValueError("Wenn ein keyfile gesetzt ist, muss auch ein certfile angegeben werden.")
        if self.certfile and not self.keyfile:
            raise ValueError("Wenn ein certfile gesetzt ist, muss auch ein keyfile angegeben werden.")


def load_config(config_path: Optional[str]) -> QuicstarConfig:
    base = QuicstarConfig.from_env()
    if config_path:
        path = Path(config_path).expanduser()
        file_config = QuicstarConfig.from_toml(path)
        merged = QuicstarConfig.merge(base, file_config)
    else:
        merged = base
    merged.ensure_valid()
    return merged
