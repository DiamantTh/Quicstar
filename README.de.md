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

## Einbindung in bestehende Projekte
1. **Quicstar als Abhängigkeit eintragen.** Installiere das Paket ins Virtualenv (`pip install quicstar`) oder trage es in `pyproject.toml` ein und sperre die Version wie gewohnt.
2. **Eine ASGI-App bereitstellen.** Django, FastAPI, Starlette & Co. bringen bereits einen ASGI-Callable mit (z. B. `myproject.asgi:application`). Eigene Projekte exportieren ihr `app`-Objekt aus einem Modul.
3. **Quicstar auf diesen Callable zeigen lassen.** Per `--app pfad.zum:callable` oder `QUICSTAR_APP` übergibst du den Einstiegspunkt. Alle übrigen Projekteinstellungen (Datenbank, Feature-Flags, Logging) bleiben dort, wo sie bisher schon lagen.
4. **Binds/Protokolle je Umgebung setzen.** Lokal reicht `localhost:8000` plus `--protocol http1`. In Produktion nutzt du etwa `--bind 0.0.0.0:443 --protocol auto --certfile ... --keyfile ...` oder die entsprechenden `QUICSTAR_*`-Variablen. Im Container landet der CLI-Aufruf einfach im Image oder in deinem `docker-compose`-Service.
5. **Optional Reload für Dev.** Mit `--reload` und `--reload-dirs` ersetzt Quicstar deinen bisherigen `uvicorn`/`hypercorn`-Dev-Server drop-in und beobachtet den Source-Tree.

Damit bleibt der Rest deines Stacks unberührt: Django-Management-Commands, Middleware und bestehende Logging-Setups funktionieren unverändert, weil Quicstar ausschließlich die ASGI-Server-Schicht austauscht.

## Standard-Endpunkte & Healthchecks
- Ohne explizites `--app` liefert Quicstar seine interne `default_app` aus, die `/` (Status-Text) sowie `/health` (Plain `ok`) bereitstellt. `/health` eignet sich als Probe-Endpunkt für Container-Orchestrierung oder Load-Balancer.
- Sobald du deine eigene ASGI-App angibst, bekommst du exakt deren Routen. Quicstar reicht die Requests nur durch – Versionierung, API-Prefixe oder WebSockets funktionieren identisch wie unter anderen ASGI-Servern.
- Möchtest du weiterhin einen leichten Health-Endpunkt haben, häng ihn einfach in deine ASGI-App (z. B. zusätzliche Django-View) oder reserviere einen dedizierten `health`-Pfad, damit Proxies und Monitore eine stabile URL behalten.

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
