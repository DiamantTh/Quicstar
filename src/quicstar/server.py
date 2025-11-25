from __future__ import annotations

import asyncio
import os
import platform
import sys
from importlib import import_module
from typing import Any, Awaitable, Callable, Dict

from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig

from .config import QuicstarConfig


ASGIApp = Callable[[Dict[str, Any], Any, Any], Awaitable[None]]


def load_asgi_app(app_ref: Any) -> ASGIApp:
    """Resolve a string like 'module:app' into an ASGI callable."""
    if callable(app_ref):
        return app_ref  # already a callable

    if isinstance(app_ref, str):
        if ":" not in app_ref:
            raise ValueError("ASGI path must be in the form 'module:attribute'")
        module_name, attr_name = app_ref.split(":", 1)
        module = import_module(module_name)
        app = getattr(module, attr_name)
        if not callable(app):
            raise TypeError(f"Attribute '{attr_name}' in '{module_name}' is not callable")
        return app

    raise TypeError("app reference must be a callable or import path string")


async def default_app(scope: Dict[str, Any], receive, send) -> None:
    if scope["type"] != "http":
        raise RuntimeError("default_app supports only HTTP scope.")

    info = [
        "Quicstar is running.",
        f"Python: {sys.version.split()[0]}",
        f"Platform: {platform.platform()}",
        f"PID: {os.getpid()}",
    ]
    body = ("\n".join(info)).encode("utf-8")

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain; charset=utf-8")],
        }
    )
    await send({"type": "http.response.body", "body": body})


def build_hypercorn_config(settings: QuicstarConfig) -> HypercornConfig:
    cfg = HypercornConfig()
    # Bind to both stacks when unspecified/any is requested.
    if settings.host in {"0.0.0.0", "::"}:
        cfg.bind = [f"[::]:{settings.port}", f"0.0.0.0:{settings.port}"]
    else:
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

    app = load_asgi_app(settings.app)
    asyncio.run(serve(app, hypercorn_cfg))


__all__ = ["serve_app", "build_hypercorn_config", "default_app"]
