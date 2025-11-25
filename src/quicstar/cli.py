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
        description=t("cli.description"),
    )
    parser.add_argument("--config", type=Path, help=t("cli.config"))
    parser.add_argument("--host", help=t("cli.host"))
    parser.add_argument("--port", type=int, help=t("cli.port"))
    parser.add_argument("--app", help=t("cli.app"))
    parser.add_argument(
        "--protocol",
        choices=["auto", "http3", "http1"],
        help=t("cli.protocol"),
    )
    parser.add_argument("--workers", type=int, help=t("cli.workers"))
    parser.add_argument("--no-access-log", action="store_true", help=t("cli.no_access_log"))
    parser.add_argument("--log-level", choices=["debug", "info", "warning", "error", "critical"], help=t("cli.log_level"))
    parser.add_argument("--certfile", type=Path, help=t("cli.certfile"))
    parser.add_argument("--keyfile", type=Path, help=t("cli.keyfile"))
    parser.add_argument("--quic-bind", help=t("cli.quic_bind"))
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
