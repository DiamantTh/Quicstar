from __future__ import annotations

import argparse
from pathlib import Path

from .config import QuicstarConfig, load_config
from .i18n import get_translator
from .server import serve_app


def _build_parser() -> argparse.ArgumentParser:
    t, _ = get_translator()
    parser = argparse.ArgumentParser(
        prog="quicstar",
        description=t("Lightweight HTTP/3 server with TOML configuration and Traefik-friendly defaults."),
    )
    parser.add_argument("--config", type=Path, help=t("Path to a TOML file (standalone mode)"))
    parser.add_argument("--host", help=t("Host/IP to bind HTTP (deprecated, use --bind)"))
    parser.add_argument(
        "--bind",
        action="append",
        help="Bind address, e.g. 0.0.0.0:8000, [::]:8000 (can be used multiple times)",
    )
    parser.add_argument("--port", type=int, help=t("Port to bind HTTP"))
    parser.add_argument("--app", help=t("ASGI path, e.g. myproject.asgi:application"))
    parser.add_argument(
        "--protocol",
        choices=["auto", "http3", "http1"],
        help=t("Protocol selection (HTTP/3, HTTP/1.1 only, or automatic)"),
    )
    parser.add_argument("--backlog", type=int, help="Socket listen backlog")
    parser.add_argument("--workers", type=int, help=t("Number of worker processes"))
    parser.add_argument("--no-access-log", action="store_true", help=t("Disable access logs"))
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        help=t("Log level"),
    )
    parser.add_argument("--certfile", type=Path, help=t("TLS certificate (required for HTTP/3)"))
    parser.add_argument("--keyfile", type=Path, help=t("TLS key (required for HTTP/3)"))
    parser.add_argument("--quic-bind", help=t("Optional QUIC bind, e.g. '0.0.0.0:443'"))
    return parser


def _apply_overrides(base: QuicstarConfig, args: argparse.Namespace) -> QuicstarConfig:
    overrides = {
        "host": args.host,
        "port": args.port,
        "binds": args.bind,
        "app": args.app,
        "protocol_mode": args.protocol,
        "workers": args.workers,
        "backlog": args.backlog,
        "access_log": None if args.no_access_log is False else False,
        "log_level": args.log_level,
        "certfile": args.certfile,
        "keyfile": args.keyfile,
        "quic_bind": args.quic_bind,
    }
    filtered = {k: v for k, v in overrides.items() if v is not None}
    merged = QuicstarConfig.merge(base, QuicstarConfig(**filtered))
    merged.ensure_valid()
    return merged


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    settings = load_config(str(args.config)) if args.config else load_config(None)
    settings = _apply_overrides(settings, args)

    serve_app(settings)


__all__ = ["main"]
