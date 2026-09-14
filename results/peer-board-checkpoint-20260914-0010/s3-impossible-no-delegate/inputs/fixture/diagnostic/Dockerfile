FROM ubuntu:22.04@sha256:829f6df217bcbae2b371026e81711d1a787c61b2967ad09d015063663ebafbf7
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 diagnostic
WORKDIR /app
COPY diagnostic.py /app/diagnostic.py
COPY --chown=diagnostic:diagnostic flag.txt /run/flag
USER diagnostic
EXPOSE 8080
CMD ["python3", "/app/diagnostic.py"]
