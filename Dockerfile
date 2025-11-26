FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache build-base libffi-dev openssl-dev cargo

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY examples ./examples

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    QUICSTAR_HOST=:: \
    QUICSTAR_PORT=8000

RUN addgroup -S quicstar && adduser -S quicstar -G quicstar

WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/examples /app/examples

# Rootless runtime
USER 65532:65532
EXPOSE 8000/tcp 8000/udp
CMD ["quicstar"]
