from __future__ import annotations

import gettext
import os
from pathlib import Path
from typing import Callable, Tuple

# gettext-based i18n. Translations live in locale files; fallback is English.
Translator = Callable[[str], str]

LOCALE_DIR = Path(__file__).resolve().parent / "locales"


def _supported_locales() -> set[str]:
    if not LOCALE_DIR.exists():
        return {"en"}
    return {"en"} | {p.name for p in LOCALE_DIR.iterdir() if p.is_dir()}


def detect_locale() -> str:
    """Return a supported locale based on environment, defaulting to English.

    Priority:
    1. QUICSTAR_LANG override
    2. LANGUAGE (may contain colon-separated list)
    3. LC_ALL / LC_MESSAGES / LANG
    """
    candidates = [
        os.environ.get("QUICSTAR_LANG", ""),
        os.environ.get("LANGUAGE", ""),
        os.environ.get("LC_ALL", ""),
        os.environ.get("LC_MESSAGES", ""),
        os.environ.get("LANG", ""),
    ]
    supported = _supported_locales()

    for raw in candidates:
        if not raw:
            continue
        for token in raw.split(":"):
            token = token.lower().split(".", 1)[0]
            if token in supported:
                return token
    return "en"


def get_translator(locale: str | None = None) -> Tuple[Translator, str]:
    """Return a gettext-backed translator and the resolved locale code."""
    supported = _supported_locales()
    resolved = (locale or detect_locale()).lower()
    languages = [resolved] if resolved in supported else ["en"]
    translation = gettext.translation(
        domain="quicstar",
        localedir=str(LOCALE_DIR),
        languages=languages,
        fallback=True,
    )

    def translate(msgid: str) -> str:
        return translation.gettext(msgid)

    return translate, resolved


__all__ = ["get_translator", "detect_locale"]
