# Our Mood – Sync-Server (läuft auch auf dem Raspberry Pi: arm64 / armv7)
FROM python:3.12-alpine

WORKDIR /app
COPY server.py /app/server.py

# Datenverzeichnis für die SQLite-Datei; Dienst läuft ohne Root-Rechte
RUN mkdir -p /data && chown nobody:nobody /data
USER nobody

ENV DB_PATH=/data/our-mood-sync.db \
    PORT=8080 \
    PYTHONUNBUFFERED=1

EXPOSE 8080
HEALTHCHECK --interval=60s --timeout=5s CMD wget -qO- http://127.0.0.1:8080/v1/health || exit 1
CMD ["python", "/app/server.py"]
