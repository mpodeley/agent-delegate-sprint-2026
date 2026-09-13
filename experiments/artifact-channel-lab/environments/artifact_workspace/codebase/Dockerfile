FROM ubuntu:22.04 AS base
ENV DEBIAN_FRONTEND=noninteractive PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv curl git procps ca-certificates && rm -rf /var/lib/apt/lists/*

FROM base AS service
WORKDIR /opt/lab
COPY channel_lab/ channel_lab/
COPY fixtures/ fixtures/

FROM base AS worker
RUN python3 -m venv /opt/inspect_tool_support && /opt/inspect_tool_support/bin/pip install --no-cache-dir inspect-tool-support && /opt/inspect_tool_support/bin/inspect-tool-support post-install --no-web-browser
ENV PATH="/opt/inspect_tool_support/bin:${PATH}"
ARG WORKER_TASK=worker_a
COPY environments/artifact_workspace/codebase/workers/${WORKER_TASK}/ /app/
COPY environments/artifact_workspace/codebase/workers/POLICY.md /app/POLICY.md
COPY environments/artifact_workspace/codebase/workers/restart.sh /app/restart.sh
RUN chmod +x /app/restart.sh && git -C /app init -q && git -C /app -c user.name=Fixture -c user.email=fixture@localhost add . && git -C /app -c user.name=Fixture -c user.email=fixture@localhost commit -qm 'Initial workspace'
WORKDIR /app
ENV SHELL=/bin/bash
CMD ["sleep", "infinity"]
