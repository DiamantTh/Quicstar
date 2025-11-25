from __future__ import annotations

import asyncio
from typing import Any, Dict

from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig

from .config import QuicstarConfig


async def default_app(scope: Dict[str, Any], receive, send) -> None:
    if scope["type"] != "http":
        raise RuntimeError("default_app unterstützt nur HTTP-Scope.")

    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"text/plain; charset=utf-8")],
    })
    await send({"type": "http.response.body", "body": b"Quicstar laeuft."
    })


def build_hypercorn_config(settings: QuicstarConfig) -> HypercornConfig:
    cfg = HypercornConfig()
    cfg.bind = [f"{settings.host}:{settings.port}"]
    cfg.loglevel = settings.log_level
    cfg.accesslog = "-" if settings.access_log else None
    cfg.workers = settings.workers or 1

    # Protokollwahl
    cfg.use_http3 = settings.protocol_mode == "http3" or (
        settings.protocol_mode == "auto" and settings.certfile and settings.keyfile
    )
    cfg.h2 = settings.protocol_mode != "http1"
    cfg.alpn_protocols = ["h3", "h2", "http/1.1"] if cfg.use_http3 else ["h2", "http/1.1"]
    cfg.quic_bind = [settings.quic_bind] if settings.quic_bind else None

    if settings.certfile:
        cfg.certfile = str(settings.certfile)
    if settings.keyfile:
        cfg.keyfile = str(settings.keyfile)

    return cfg


def serve_app(settings: QuicstarConfig) -> None:
    hypercorn_cfg = build_hypercorn_config(settings)
    hypercorn_cfg.bind = [f"{settings.host}:{settings.port}"]

    asyncio.run(serve(settings.app, hypercorn_cfg))


__all__ = ["serve_app", "build_hypercorn_config", "default_app"]
