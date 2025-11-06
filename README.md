![PyTorrent logo](static/img/pytorrent-logo.webp)

# PyTorrent

PyTorrent is a simple BitTorrent downloader with web ui written in Python using libtorrent.

You can run it locally on your computer or on a NAS/VPS/homelab as a container or Systemd service.

## Run locally

```bash
python3 app.py
```

## Run using Docker

### Build image

```bash
docker build . -t PyTorrent:latest
```

### Run container

```bash
docker run -d \
  -p 6767:6767 \
  -p 6881:6881 \
  -p 6891:6891 \
  -v $(pwd)/downloads:/downloads \
  -v $(pwd)/torrents:/torrents \
  PyTorrent:atest
```

## Run using Systemd

- Clone this repo to `/opt/pytorrent`
- Copy the `pytorrent.service` file to `/etc/systemd/system` 
- Reload systemd services by running `systemctl daemon-reload`
- Enable and start the service ny running `systemcl enable pytorrent --now`

## Connect to the web ui

Open your browser and go to `http://127.0.0.1:6767` if you run it locally
(Replace `127.0.0.1` by the IP of your server if you're not running locally)

### Download dir

- If you run PyTorrent using the Python script locally the `downloads` dir will be created as a subdir of your PWD
- If you run PyTorrent using Docker it will be `/downloads` in the dir, which is bind mounted to a `downloads` dir under your PWD when using the command above (so practically the same as running it locally)
- When you run PyTorrent as a Systemd service, downloads will appear under `/var/lib/pytorrent/downloads`. You can adjust this be changing the value of `Environment=DOWNLOAD_DIR` in your `.service` file. Keep in mind the `pytorrent` user will need write permissions to this directory.
