# Quicstar

Quicstar ist ein leichtgewichtiges, per `pip` installierbares Python-Paket mit integriertem Webserver. Der Server spricht moderne Protokolle (HTTP/1.1, HTTP/2 und HTTP/3/QUIC), lässt sich in Docker- und Traefik-Setups betreiben und kann sowohl standalone als auch mit Frameworks wie Django genutzt werden.

## Features
- **HTTP/3 & QUIC** inklusive ALPN; reiner HTTP/1.1-Modus konfigurierbar.
- **Framework-kompatibel:** übernimmt beliebige ASGI-Apps (z. B. `myproject.asgi:application`).
- **Multi-Core ready:** Worker-Anzahl konfigurierbar, standardmäßig entsprechend CPU-Kernen.
- **Containerfreundlich:** liest Environment-Variablen und TOML-Configs; solide Defaults für Traefik/Docker.
- **TLS bereit:** Zertifikat/Key können gesetzt werden; für HTTP/3 zwingend notwendig.
- **Geringer Overhead:** basiert auf Hypercorn, beherrscht auch HTTP/2 und WebSockets.

## Installation
```bash
pip install .
```

## Standalone starten
```bash
quicstar --config examples/quicstar.example.toml
```

Ohne Config greift der Server auf Environment-Variablen zurück und startet die interne Minimal-App:
```bash
QUICSTAR_HOST=0.0.0.0 QUICSTAR_PORT=8000 quicstar --protocol http1
```

Wichtige Optionen (auch per Env möglich):
- `--app` / `QUICSTAR_APP`: ASGI-Pfad, z. B. Django `myproject.asgi:application`.
- `--protocol` / `QUICSTAR_PROTOCOL`: `auto`, `http3` oder `http1`.
- `--certfile`, `--keyfile`: TLS-Dateien für HTTP/3/QUIC.
- `--quic-bind`: separater QUIC-Port, falls Traefik TLS terminiert.
- `--workers`: Anzahl Prozesse für Mehrkernbetrieb.

## Einsatz mit Django/anderen Frameworks
Binde einfach die ASGI-App deiner Anwendung ein:
```bash
quicstar --app myproject.asgi:application --protocol auto --certfile /certs/fullchain.pem --keyfile /certs/privkey.pem
```

Die jeweilige Framework-Konfiguration (Settings, Logging etc.) bleibt unangetastet; Quicstar übernimmt nur das Serving.

## Konfiguration per TOML
Siehe `examples/quicstar.example.toml` für eine menschenlesbare Konfiguration. Die Datei steuert ausschließlich den Standalone-Betrieb.

## Docker & Traefik Hinweise
- Standard-Bind ist `0.0.0.0`, dadurch containerfreundlich.
- Für Traefik kann `--quic-bind` genutzt werden, falls ein separater QUIC-Port notwendig ist.
- Zertifikate können über gemountete Volumes eingebunden werden.

## HTTP/1.1-only Modus
Setze `--protocol http1` oder `QUICSTAR_PROTOCOL=http1`, um nur HTTP/1.1 zu bedienen (z. B. für minimalen Speicherbedarf oder alte Clients).

## Weitere Protokolle
Hypercorn unterstützt HTTP/2 und WebSockets automatisch; QUIC wird bei gesetzten Zertifikaten aktiv.
