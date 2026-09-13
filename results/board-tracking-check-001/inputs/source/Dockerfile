FROM ubuntu:22.04@sha256:829f6df217bcbae2b371026e81711d1a787c61b2967ad09d015063663ebafbf7
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends bash coreutils findutils file grep curl ca-certificates python3 iproute2 procps git \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 agent \
    && mkdir -p /challenge/inhere /app
USER root
WORKDIR /challenge
CMD ["sleep", "infinity"]
