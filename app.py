import libtorrent as lt
import time
import threading
import os
from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)
DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "downloads")
TORRENT_DIR = os.environ.get("TORRENT_DIR", "torrents")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(TORRENT_DIR, exist_ok=True)

# Global variables
session = lt.session()
session.listen_on(6881, 6891)
torrent_handle = None
status_data = {"progress": 0, "download_rate": 0, "upload_rate": 0, "peers": 0, "name": "", "state": "idle"}

def download_torrent(info):
    """Runs torrent download loop in background thread."""
    global torrent_handle
    h = session.add_torrent(info)
    status_data["name"] = h.name()
    print(f"Downloading: {h.name()}")

    while not h.is_seed():
        s = h.status()
        status_data.update({
            "progress": s.progress * 100,
            "download_rate": s.download_rate / 1000,
            "upload_rate": s.upload_rate / 1000,
            "peers": s.num_peers,
            "state": str(s.state)
        })
        time.sleep(1)

    status_data["state"] = "complete"
    print("Download complete.")

@app.route("/")
def index():
    return render_template("index.html", status=status_data)

@app.route("/status")
def status():
    return jsonify(status_data)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("torrent_file")
    magnet = request.form.get("magnet_url")

    if file:
        save_path = os.path.join(TORRENT_DIR, file.filename)
        file.save(save_path)
        info = lt.torrent_info(save_path)
        params = {"save_path": DOWNLOAD_DIR, "ti": info}
        threading.Thread(target=download_torrent, args=(params,), daemon=True).start()
        return redirect(url_for("index"))

    elif magnet:
        params = {"save_path": DOWNLOAD_DIR, "url": magnet}
        threading.Thread(target=download_torrent, args=(params,), daemon=True).start()
        return redirect(url_for("index"))

    return "No input provided", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6767, debug=True)
