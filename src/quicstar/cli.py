from __future__ import annotations

import argparse
from pathlib import Path

from .config import QuicstarConfig, load_config
from .server import serve_app


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quicstar",
        description="Leichter HTTP/3-Server mit TOML-Konfiguration und Traefik-kompatiblen Defaults.",
    )
    parser.add_argument("--config", type=Path, help="Pfad zu einer TOML-Datei (Standalone-Modus)")
    parser.add_argument("--host", help="Host/IP fuer den HTTP-Bind")
    parser.add_argument("--port", type=int, help="Port fuer den HTTP-Bind")
    parser.add_argument("--app", help="ASGI-Pfad, z. B. myproject.asgi:application")
    parser.add_argument(
        "--protocol",
        choices=["auto", "http3", "http1"],
        help="Explizite Protokollwahl (HTTP/3, nur HTTP/1.1 oder automatisch)",
    )
    parser.add_argument("--workers", type=int, help="Anzahl der Worker-Prozesse")
    parser.add_argument("--no-access-log", action="store_true", help="Access-Logs deaktivieren")
    parser.add_argument("--log-level", choices=["debug", "info", "warning", "error", "critical"], help="Log-Level")
    parser.add_argument("--certfile", type=Path, help="TLS Zertifikat (erforderlich fuer HTTP/3)")
    parser.add_argument("--keyfile", type=Path, help="TLS Key (erforderlich fuer HTTP/3)")
    parser.add_argument("--quic-bind", help="Optionaler QUIC-Bind, z. B. '0.0.0.0:443'")
    return parser


def _apply_overrides(base: QuicstarConfig, args: argparse.Namespace) -> QuicstarConfig:
    overrides = {
        "host": args.host,
        "port": args.port,
        "app": args.app,
        "protocol_mode": args.protocol,
        "workers": args.workers,
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
