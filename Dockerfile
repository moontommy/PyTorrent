FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    python3-libtorrent \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app.py /app/
COPY templates /app/templates
COPY static /app/static

RUN pip install flask

ENV DOWNLOAD_DIR=/downloads
ENV TORRENT_DIR=/torrents

EXPOSE 6767 6881 6891

VOLUME ["/downloads", "/torrents"]

CMD ["python", "app.py"]
