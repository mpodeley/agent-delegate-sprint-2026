FROM ubuntu:22.04 AS base
ENV DEBIAN_FRONTEND=noninteractive PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends python3 curl git ca-certificates && rm -rf /var/lib/apt/lists/*
FROM base AS service
WORKDIR /opt/lab
COPY channel_lab/ channel_lab/
FROM base AS worker
RUN useradd -m -u 1000 worker
COPY --chown=worker:worker environments/artifact_attestation/codebase/workers/ /app/
WORKDIR /app
USER worker
ENV SHELL=/bin/bash
CMD ["sleep", "infinity"]
