from __future__ import annotations

import gettext
import os
from pathlib import Path
from typing import Callable, Dict, Tuple

# gettext-based i18n with a built-in dictionary fallback for known languages.
Translations = Dict[str, str]
Translator = Callable[[str], str]

# msgids are the English strings used directly in code.
TRANSLATIONS: Dict[str, Translations] = {
    "de": {
        "Lightweight HTTP/3 server with TOML configuration and Traefik-friendly defaults.": "Leichter HTTP/3-Server mit TOML-Konfiguration und Traefik-kompatiblen Defaults.",
        "Path to a TOML file (standalone mode)": "Pfad zu einer TOML-Datei (Standalone-Modus)",
        "Host/IP to bind HTTP": "Host/IP fuer den HTTP-Bind",
        "Port to bind HTTP": "Port fuer den HTTP-Bind",
        "ASGI path, e.g. myproject.asgi:application": "ASGI-Pfad, z. B. myproject.asgi:application",
        "Protocol selection (HTTP/3, HTTP/1.1 only, or automatic)": "Protokollwahl (HTTP/3, nur HTTP/1.1 oder automatisch)",
        "Number of worker processes": "Anzahl der Worker-Prozesse",
        "Disable access logs": "Access-Logs deaktivieren",
        "Log level": "Log-Level",
        "TLS certificate (required for HTTP/3)": "TLS Zertifikat (erforderlich fuer HTTP/3)",
        "TLS key (required for HTTP/3)": "TLS Key (erforderlich fuer HTTP/3)",
        "Optional QUIC bind, e.g. '0.0.0.0:443'": "Optionaler QUIC-Bind, z. B. '0.0.0.0:443'",
        "protocol_mode must be one of: auto, http3, http1": "protocol_mode muss eine dieser Optionen sein: auto, http3, http1",
        "TLS certificate (certfile) is required for HTTP/3.": "Fuer HTTP/3 muss ein TLS-Zertifikat (certfile) angegeben werden.",
        "If a keyfile is set, a certfile must also be provided.": "Wenn ein keyfile gesetzt ist, muss auch ein certfile angegeben werden.",
        "If a certfile is set, a keyfile must also be provided.": "Wenn ein certfile gesetzt ist, muss auch ein keyfile angegeben werden.",
    },
    "es": {
        "Lightweight HTTP/3 server with TOML configuration and Traefik-friendly defaults.": "Servidor HTTP/3 ligero con configuracion TOML y defaults compatibles con Traefik.",
        "Path to a TOML file (standalone mode)": "Ruta a un archivo TOML (modo standalone)",
        "Host/IP to bind HTTP": "Host/IP para el bind HTTP",
        "Port to bind HTTP": "Puerto para el bind HTTP",
        "ASGI path, e.g. myproject.asgi:application": "Ruta ASGI, p. ej. myproject.asgi:application",
        "Protocol selection (HTTP/3, HTTP/1.1 only, or automatic)": "Seleccion de protocolo (HTTP/3, solo HTTP/1.1 o automatico)",
        "Number of worker processes": "Numero de procesos worker",
        "Disable access logs": "Desactivar access logs",
        "Log level": "Nivel de log",
        "TLS certificate (required for HTTP/3)": "Certificado TLS (requerido para HTTP/3)",
        "TLS key (required for HTTP/3)": "Clave TLS (requerida para HTTP/3)",
        "Optional QUIC bind, e.g. '0.0.0.0:443'": "Bind QUIC opcional, p. ej. '0.0.0.0:443'",
        "protocol_mode must be one of: auto, http3, http1": "protocol_mode debe ser: auto, http3 o http1",
        "TLS certificate (certfile) is required for HTTP/3.": "Se requiere un certificado TLS (certfile) para HTTP/3.",
        "If a keyfile is set, a certfile must also be provided.": "Si se define keyfile, tambien se debe definir certfile.",
        "If a certfile is set, a keyfile must also be provided.": "Si se define certfile, tambien se debe definir keyfile.",
    },
    "fr": {
        "Lightweight HTTP/3 server with TOML configuration and Traefik-friendly defaults.": "Serveur HTTP/3 leger avec configuration TOML et defaults compatibles Traefik.",
        "Path to a TOML file (standalone mode)": "Chemin vers un fichier TOML (mode autonome)",
        "Host/IP to bind HTTP": "Hote/IP pour le bind HTTP",
        "Port to bind HTTP": "Port pour le bind HTTP",
        "ASGI path, e.g. myproject.asgi:application": "Chemin ASGI, ex. myproject.asgi:application",
        "Protocol selection (HTTP/3, HTTP/1.1 only, or automatic)": "Selection du protocole (HTTP/3, HTTP/1.1 seul ou automatique)",
        "Number of worker processes": "Nombre de processus worker",
        "Disable access logs": "Desactiver les access logs",
        "Log level": "Niveau de log",
        "TLS certificate (required for HTTP/3)": "Certificat TLS (requis pour HTTP/3)",
        "TLS key (required for HTTP/3)": "Cle TLS (requise pour HTTP/3)",
        "Optional QUIC bind, e.g. '0.0.0.0:443'": "Bind QUIC optionnel, ex. '0.0.0.0:443'",
        "protocol_mode must be one of: auto, http3, http1": "protocol_mode doit etre: auto, http3 ou http1",
        "TLS certificate (certfile) is required for HTTP/3.": "Un certificat TLS (certfile) est requis pour HTTP/3.",
        "If a keyfile is set, a certfile must also be provided.": "Si un keyfile est defini, un certfile doit aussi etre defini.",
        "If a certfile is set, a keyfile must also be provided.": "Si un certfile est defini, un keyfile doit aussi etre defini.",
    },
    "ja": {
        "Lightweight HTTP/3 server with TOML configuration and Traefik-friendly defaults.": "軽量なHTTP/3サーバー。TOML設定とTraefik向けデフォルトを備える。",
        "Path to a TOML file (standalone mode)": "TOMLファイルへのパス（スタンドアロンモード）",
        "Host/IP to bind HTTP": "HTTPでバインドするホスト/IP",
        "Port to bind HTTP": "HTTPでバインドするポート",
        "ASGI path, e.g. myproject.asgi:application": "ASGIパス（例: myproject.asgi:application）",
        "Protocol selection (HTTP/3, HTTP/1.1 only, or automatic)": "プロトコル選択（HTTP/3、HTTP/1.1のみ、または自動）",
        "Number of worker processes": "ワーカープロセス数",
        "Disable access logs": "アクセスログを無効化",
        "Log level": "ログレベル",
        "TLS certificate (required for HTTP/3)": "TLS証明書（HTTP/3に必須）",
        "TLS key (required for HTTP/3)": "TLS秘密鍵（HTTP/3に必須）",
        "Optional QUIC bind, e.g. '0.0.0.0:443'": "任意のQUICバインド（例: '0.0.0.0:443'）",
        "protocol_mode must be one of: auto, http3, http1": "protocol_mode は auto/http3/http1 のいずれかにしてください",
        "TLS certificate (certfile) is required for HTTP/3.": "HTTP/3 には TLS 証明書 (certfile) が必要です。",
        "If a keyfile is set, a certfile must also be provided.": "keyfile を設定する場合、certfile も必要です。",
        "If a certfile is set, a keyfile must also be provided.": "certfile を設定する場合、keyfile も必要です。",
    },
    "zh": {
        "Lightweight HTTP/3 server with TOML configuration and Traefik-friendly defaults.": "Qingliang HTTP/3 fuwuqi, TOML peizhi he Traefik you hao moren.",
        "Path to a TOML file (standalone mode)": "TOML wenjian de lujing (duli moshi)",
        "Host/IP to bind HTTP": "HTTP bangding de host/IP",
        "Port to bind HTTP": "HTTP bangding de duankou",
        "ASGI path, e.g. myproject.asgi:application": "ASGI lujing, li ru myproject.asgi:application",
        "Protocol selection (HTTP/3, HTTP/1.1 only, or automatic)": "Xieyi xuanze (HTTP/3, zhiyou HTTP/1.1, huozhe zidong)",
        "Number of worker processes": "Worker jincheng shu",
        "Disable access logs": "Jinyong access log",
        "Log level": "Rizhi dengji",
        "TLS certificate (required for HTTP/3)": "TLS zhengshu (HTTP/3 bixu)",
        "TLS key (required for HTTP/3)": "TLS miyao (HTTP/3 bixu)",
        "Optional QUIC bind, e.g. '0.0.0.0:443'": "Kexuan QUIC bangding, li ru '0.0.0.0:443'",
        "protocol_mode must be one of: auto, http3, http1": "protocol_mode ying wei auto/http3/http1 qi zhong yi ge",
        "TLS certificate (certfile) is required for HTTP/3.": "HTTP/3 xuyao TLS zhengshu (certfile).",
        "If a keyfile is set, a certfile must also be provided.": "She zhi keyfile shi bixu tongshi she zhi certfile.",
        "If a certfile is set, a keyfile must also be provided.": "She zhi certfile shi bixu tongshi she zhi keyfile.",
    },
}

SUPPORTED = set(TRANSLATIONS.keys()) | {"en"}
LOCALE_DIR = Path(__file__).resolve().parent / "locales"


def detect_locale() -> str:
    """Return a supported locale based on environment, defaulting to English.

    Priority:
    1. QUICSTAR_LANG override
    2. LANGUAGE (may contain colon-separated list)
    3. LC_ALL / LC_MESSAGES / LANG
    """
    env_vars = [
        os.environ.get("QUICSTAR_LANG", ""),
        os.environ.get("LANGUAGE", ""),
        os.environ.get("LC_ALL", ""),
        os.environ.get("LC_MESSAGES", ""),
        os.environ.get("LANG", ""),
    ]

    for raw in env_vars:
        if not raw:
            continue
        for token in raw.split(":"):
            token = token.lower().split(".", 1)[0]
            if token in SUPPORTED:
                return token
    return "en"


def get_translator(locale: str | None = None) -> Tuple[Translator, str]:
    """Return a gettext-backed translator and the resolved locale code."""
    resolved = (locale or detect_locale()).lower()
    languages = [resolved] if resolved in SUPPORTED else ["en"]
    translation = gettext.translation(
        domain="quicstar",
        localedir=str(LOCALE_DIR),
        languages=languages,
        fallback=True,
    )
    fallback = TRANSLATIONS.get(resolved, {})

    def translate(msgid: str) -> str:
        text = translation.gettext(msgid)
        if text != msgid or resolved == "en":
            return text
        return fallback.get(msgid, text)

    return translate, resolved


__all__ = ["get_translator", "detect_locale"]
