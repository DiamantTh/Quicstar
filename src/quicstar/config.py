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

from .i18n import get_translator


DEFAULT_HOST = "::1"
DEFAULT_PORT = 8000
DEFAULT_APP = "quicstar.server:default_app"


@dataclass
class QuicstarConfig:
    """Configuration for the Quicstar server."""

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    binds: Optional[list[str]] = None
    app: str = DEFAULT_APP
    protocol_mode: str = "auto"  # auto|http3|http1
    workers: int = field(default_factory=os.cpu_count)
    backlog: Optional[int] = None
    access_log: bool = True
    log_level: str = "info"
    proxy_headers: bool = False
    forwarded_allow_ips: Optional[str] = None
    forwarded_allow_ips_file: Optional[Path] = None
    access_log_format: Optional[str] = None
    keep_alive_timeout: Optional[int] = None
    graceful_timeout: Optional[int] = None
    shutdown_timeout: Optional[int] = None
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
        env_binds = os.getenv("QUICSTAR_BINDS")
        binds = [b for b in env_binds.split(",") if b] if env_binds else None
        return cls(
            host=os.getenv("QUICSTAR_HOST", DEFAULT_HOST),
            port=int(os.getenv("QUICSTAR_PORT", DEFAULT_PORT)),
            app=os.getenv("QUICSTAR_APP", DEFAULT_APP),
            protocol_mode=os.getenv("QUICSTAR_PROTOCOL", "auto"),
            workers=int(os.getenv("QUICSTAR_WORKERS", os.cpu_count() or 1)),
            backlog=int(os.getenv("QUICSTAR_BACKLOG", "0")) or None,
            access_log=os.getenv("QUICSTAR_ACCESS_LOG", "true").lower() == "true",
            log_level=os.getenv("QUICSTAR_LOG_LEVEL", "info"),
            proxy_headers=os.getenv("QUICSTAR_PROXY_HEADERS", "false").lower() == "true",
            forwarded_allow_ips=os.getenv("QUICSTAR_FORWARDED_ALLOW_IPS"),
            forwarded_allow_ips_file=cls._maybe_path(os.getenv("QUICSTAR_FORWARDED_ALLOW_IPS_FILE")),
            access_log_format=os.getenv("QUICSTAR_ACCESS_LOG_FORMAT"),
            keep_alive_timeout=int(os.getenv("QUICSTAR_KEEP_ALIVE", "0")) or None,
            graceful_timeout=int(os.getenv("QUICSTAR_GRACEFUL_TIMEOUT", "0")) or None,
            shutdown_timeout=int(os.getenv("QUICSTAR_SHUTDOWN_TIMEOUT", "0")) or None,
            certfile=cls._maybe_path(os.getenv("QUICSTAR_CERTFILE")),
            keyfile=cls._maybe_path(os.getenv("QUICSTAR_KEYFILE")),
            quic_bind=os.getenv("QUICSTAR_QUIC_BIND"),
            binds=binds,
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
        t, _ = get_translator()
        valid_modes = {"auto", "http3", "http1"}
        if self.protocol_mode not in valid_modes:
            raise ValueError(t("protocol_mode must be one of: auto, http3, http1"))
        if self.protocol_mode == "http3" and not self.certfile:
            raise ValueError(t("TLS certificate (certfile) is required for HTTP/3."))
        if self.keyfile and not self.certfile:
            raise ValueError(t("If a keyfile is set, a certfile must also be provided."))
        if self.certfile and not self.keyfile:
            raise ValueError(t("If a certfile is set, a keyfile must also be provided."))
        if self.binds:
            for entry in self.binds:
                if ":" not in entry:
                    raise ValueError(f"Invalid bind '{entry}'; use host:port or [::]:port")


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
