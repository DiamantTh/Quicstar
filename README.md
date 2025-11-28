# Quicstar

Quicstar is a lightweight Python package with a built-in web server that ships as a simple `pip` install. The server speaks modern protocols (HTTP/1.1, HTTP/2, HTTP/3/QUIC), runs comfortably behind Traefik or inside Docker, and can host standalone apps or framework ASGI apps such as Django.

## Features
- **HTTP/3 & QUIC** with ALPN; configurable HTTP/1.1-only mode.
- **Framework-friendly:** serves any ASGI app (for example `myproject.asgi:application`).
- **Multi-core ready:** worker count configurable; defaults to CPU core count.
- **Container-ready:** reads environment variables and TOML configs; sane defaults for Traefik/Docker.
- **TLS ready:** certificate/key support (required for HTTP/3/QUIC).
- **Low overhead:** built on Hypercorn, also handling HTTP/2 and WebSockets.

## Installation
```bash
pip install .
```

## Run standalone
```bash
quicstar --config examples/quicstar.example.toml
```

Without a config file, Quicstar uses environment variables and launches the internal minimal app:
```bash
QUICSTAR_HOST=0.0.0.0 QUICSTAR_PORT=8000 quicstar --protocol http1
```

Key options (also available via env vars):
- `--app` / `QUICSTAR_APP`: ASGI path, e.g., Django `myproject.asgi:application`.
- `--protocol` / `QUICSTAR_PROTOCOL`: `auto`, `http3`, or `http1`.
- `--certfile`, `--keyfile`: TLS files for HTTP/3/QUIC.
- `--quic-bind`: separate QUIC bind address if Traefik terminates TLS.
- `--workers`: number of processes for multi-core deployments.

## Using with Django or other frameworks
Point Quicstar to your ASGI app:
```bash
quicstar --app myproject.asgi:application --protocol auto --certfile /certs/fullchain.pem --keyfile /certs/privkey.pem
```

Framework-specific configuration (settings, logging, etc.) stays untouched; Quicstar only handles serving.

## Embedding into existing projects
1. **Add Quicstar as a dependency.** Either install it into the virtualenv (`pip install quicstar`) or add it to your `pyproject.toml` and lockfile.
2. **Expose an ASGI application.** Frameworks such as Django, FastAPI, Starlette, or Litestar already ship an ASGI callable (e.g., `myproject.asgi:application`). Custom projects can export their `app` object from a module.
3. **Point Quicstar to that callable.** Use `--app path.to:callable` or set `QUICSTAR_APP`. All other environment-specific settings (database URLs, feature flags, etc.) are owned by your project and can stay where they are today.
4. **Select binds/protocols per deployment target.** Local development can rely on `localhost:8000` and `--protocol http1`, while production can use `--bind 0.0.0.0:443 --protocol auto --certfile ... --keyfile ...` or the corresponding `QUICSTAR_*` variables. For container workloads, keep the CLI call inside your image or `docker-compose` service.
5. **Optional reload/dev tooling.** `--reload` and `--reload-dirs` make Quicstar watch your source tree, so you can replace a previous `uvicorn`/`hypercorn` dev server drop-in.

This approach keeps the rest of your stack unchanged: your Django `manage.py` commands, logging configuration, and middleware continue to operate exactly as before because Quicstar only replaces the ASGI server layer.

## Default endpoints & health checks
- Without an explicit `--app`, Quicstar serves its internal `default_app` that exposes `/` (status text) and `/health` (plain `ok`). The latter works well for container orchestrators or load balancers to probe the process.
- When you provide your own ASGI app, you get the exact routes that the framework defines—Quicstar simply forwards requests to it. Path mounting, versioned APIs, or WebSocket endpoints continue to behave exactly as they do under other ASGI servers.
- You can still keep the lightweight health endpoint by mounting it inside your ASGI app (e.g., an extra Django view) or by leaving a dedicated `health` route in your router so that reverse proxies and uptime monitors have a stable probe URL.

## TOML configuration
See `examples/quicstar.example.toml` for a human-readable standalone configuration.

## Docker & Traefik notes
- Default bind is `0.0.0.0`, making it container-friendly.
- Use `--quic-bind` when you need a dedicated QUIC port alongside Traefik TLS termination.
- Mount certificate volumes as needed for TLS.

## HTTP/1.1-only mode
Set `--protocol http1` or `QUICSTAR_PROTOCOL=http1` to limit serving to HTTP/1.1 (e.g., for minimal memory usage or legacy clients).

## Additional protocols
Hypercorn automatically supports HTTP/2 and WebSockets; QUIC is enabled when certificates are configured.
