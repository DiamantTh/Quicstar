from __future__ import annotations

import os
from typing import Callable, Dict, Tuple

# Simple table-based i18n. Default to English, optionally fall back to German.

Translations = Dict[str, str]
Translator = Callable[[str], str]


TRANSLATIONS: Dict[str, Translations] = {
    "en": {
        "cli.description": "Lightweight HTTP/3 server with TOML configuration and Traefik-friendly defaults.",
        "cli.host": "Host/IP to bind HTTP",
        "cli.port": "Port to bind HTTP",
        "cli.app": "ASGI path, e.g. myproject.asgi:application",
        "cli.protocol": "Protocol selection (HTTP/3, HTTP/1.1 only, or automatic)",
        "cli.workers": "Number of worker processes",
        "cli.no_access_log": "Disable access logs",
        "cli.log_level": "Log level",
        "cli.certfile": "TLS certificate (required for HTTP/3)",
        "cli.keyfile": "TLS key (required for HTTP/3)",
        "cli.quic_bind": "Optional QUIC bind, e.g. '0.0.0.0:443'",
        "error.protocol_mode": "protocol_mode must be one of: auto, http3, http1",
        "error.http3_cert": "TLS certificate (certfile) is required for HTTP/3.",
        "error.key_without_cert": "If a keyfile is set, a certfile must also be provided.",
        "error.cert_without_key": "If a certfile is set, a keyfile must also be provided.",
    },
    "de": {
        "cli.description": "Leichter HTTP/3-Server mit TOML-Konfiguration und Traefik-kompatiblen Defaults.",
        "cli.host": "Host/IP fuer den HTTP-Bind",
        "cli.port": "Port fuer den HTTP-Bind",
        "cli.app": "ASGI-Pfad, z. B. myproject.asgi:application",
        "cli.protocol": "Protokollwahl (HTTP/3, nur HTTP/1.1 oder automatisch)",
        "cli.workers": "Anzahl der Worker-Prozesse",
        "cli.no_access_log": "Access-Logs deaktivieren",
        "cli.log_level": "Log-Level",
        "cli.certfile": "TLS Zertifikat (erforderlich fuer HTTP/3)",
        "cli.keyfile": "TLS Key (erforderlich fuer HTTP/3)",
        "cli.quic_bind": "Optionaler QUIC-Bind, z. B. '0.0.0.0:443'",
        "error.protocol_mode": "protocol_mode muss eine dieser Optionen sein: auto, http3, http1",
        "error.http3_cert": "Fuer HTTP/3 muss ein TLS-Zertifikat (certfile) angegeben werden.",
        "error.key_without_cert": "Wenn ein keyfile gesetzt ist, muss auch ein certfile angegeben werden.",
        "error.cert_without_key": "Wenn ein certfile gesetzt ist, muss auch ein keyfile angegeben werden.",
    },
}


def detect_locale() -> str:
    """Return 'en' or 'de' based on environment, defaulting to English.

    Priority:
    1. QUICSTAR_LANG override
    2. LC_ALL / LC_MESSAGES / LANG
    """
    override = os.environ.get("QUICSTAR_LANG", "").lower()
    if override in ("en", "de"):
        return override

    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(var, "").lower()
        if not value:
            continue
        if value.startswith("de"):
            return "de"
        if value.startswith("en"):
            return "en"
    return "en"


def get_translator(locale: str | None = None) -> Tuple[Translator, str]:
    loc = (locale or detect_locale()).lower()
    loc = loc if loc in TRANSLATIONS else "en"
    table = TRANSLATIONS[loc]
    fallback = TRANSLATIONS["en"]

    def translate(key: str) -> str:
        return table.get(key, fallback.get(key, key))

    return translate, loc


__all__ = ["get_translator", "detect_locale"]
