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
    "es": {
        "cli.description": "Servidor HTTP/3 ligero con configuracion TOML y defaults compatibles con Traefik.",
        "cli.host": "Host/IP para el bind HTTP",
        "cli.port": "Puerto para el bind HTTP",
        "cli.app": "Ruta ASGI, p. ej. myproject.asgi:application",
        "cli.protocol": "Seleccion de protocolo (HTTP/3, solo HTTP/1.1 o automatico)",
        "cli.workers": "Numero de procesos worker",
        "cli.no_access_log": "Desactivar access logs",
        "cli.log_level": "Nivel de log",
        "cli.certfile": "Certificado TLS (requerido para HTTP/3)",
        "cli.keyfile": "Clave TLS (requerida para HTTP/3)",
        "cli.quic_bind": "Bind QUIC opcional, p. ej. '0.0.0.0:443'",
        "error.protocol_mode": "protocol_mode debe ser: auto, http3 o http1",
        "error.http3_cert": "Se requiere un certificado TLS (certfile) para HTTP/3.",
        "error.key_without_cert": "Si se define keyfile, tambien se debe definir certfile.",
        "error.cert_without_key": "Si se define certfile, tambien se debe definir keyfile.",
    },
    "fr": {
        "cli.description": "Serveur HTTP/3 leger avec configuration TOML et defaults compatibles Traefik.",
        "cli.host": "Hote/IP pour le bind HTTP",
        "cli.port": "Port pour le bind HTTP",
        "cli.app": "Chemin ASGI, ex. myproject.asgi:application",
        "cli.protocol": "Selection du protocole (HTTP/3, HTTP/1.1 seul ou automatique)",
        "cli.workers": "Nombre de processus worker",
        "cli.no_access_log": "Desactiver les access logs",
        "cli.log_level": "Niveau de log",
        "cli.certfile": "Certificat TLS (requis pour HTTP/3)",
        "cli.keyfile": "Cle TLS (requise pour HTTP/3)",
        "cli.quic_bind": "Bind QUIC optionnel, ex. '0.0.0.0:443'",
        "error.protocol_mode": "protocol_mode doit etre: auto, http3 ou http1",
        "error.http3_cert": "Un certificat TLS (certfile) est requis pour HTTP/3.",
        "error.key_without_cert": "Si un keyfile est defini, un certfile doit aussi etre defini.",
        "error.cert_without_key": "Si un certfile est defini, un keyfile doit aussi etre defini.",
    },
    "ja": {
        "cli.description": "Keiryo na HTTP/3 saabaa, TOML settei to Traefik you no default.",
        "cli.host": "HTTP bind no host/IP",
        "cli.port": "HTTP bind no port",
        "cli.app": "ASGI path, rei: myproject.asgi:application",
        "cli.protocol": "Purotokoru sentaku (HTTP/3, HTTP/1.1 nomi, mata wa auto)",
        "cli.workers": "Worker purosesu suu",
        "cli.no_access_log": "Akusesu log wo mukou ni suru",
        "cli.log_level": "Log level",
        "cli.certfile": "TLS shoumeisho (HTTP/3 ni hitsuyou)",
        "cli.keyfile": "TLS kagi (HTTP/3 ni hitsuyou)",
        "cli.quic_bind": "Nin'i no QUIC bind, rei: '0.0.0.0:443'",
        "error.protocol_mode": "protocol_mode wa auto/http3/http1 no izureka",
        "error.http3_cert": "HTTP/3 ni wa TLS shoumeisho (certfile) ga hitsuyou desu.",
        "error.key_without_cert": "Keyfile ga areba certfile mo hitsuyou desu.",
        "error.cert_without_key": "Certfile ga areba keyfile mo hitsuyou desu.",
    },
    "zh": {
        "cli.description": "Qingliang HTTP/3 fuwuqi, TOML peizhi he Traefik you hao moren.",
        "cli.host": "HTTP bangding de host/IP",
        "cli.port": "HTTP bangding de duankou",
        "cli.app": "ASGI lujing, li ru myproject.asgi:application",
        "cli.protocol": "Xieyi xuanze (HTTP/3, zhiyou HTTP/1.1, huozhe zidong)",
        "cli.workers": "Worker jincheng shu",
        "cli.no_access_log": "Jinyong access log",
        "cli.log_level": "Rizhi dengji",
        "cli.certfile": "TLS zhengshu (HTTP/3 bixu)",
        "cli.keyfile": "TLS miyao (HTTP/3 bixu)",
        "cli.quic_bind": "Kexuan QUIC bangding, li ru '0.0.0.0:443'",
        "error.protocol_mode": "protocol_mode ying wei auto/http3/http1 qi zhong yi ge",
        "error.http3_cert": "HTTP/3 xuyao TLS zhengshu (certfile).",
        "error.key_without_cert": "She zhi keyfile shi bixu tongshi she zhi certfile.",
        "error.cert_without_key": "She zhi certfile shi bixu tongshi she zhi keyfile.",
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
    """Return a supported locale based on environment, defaulting to English.

    Priority:
    1. QUICSTAR_LANG override
    2. LC_ALL / LC_MESSAGES / LANG
    """
    override = os.environ.get("QUICSTAR_LANG", "").lower()
    if override in TRANSLATIONS:
        return override

    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(var, "").lower()
        if not value:
            continue
        for code in TRANSLATIONS:
            if value.startswith(code):
                return code
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
