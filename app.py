from flask import Flask, send_file, request, abort
from datetime import datetime
import requests
import os

app = Flask(__name__)
LOG_FILE = "log.txt"
IMAGE_FILE = "quote.jpg"

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").write("=== Visitor Log Start ===\n")

@app.route('/track-image')
def track_image():
    print("=== [/track-image] Route Triggered ===")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "Unknown")
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[TRACKED] {time}, IP: {ip}, UA: {ua}")
    try:
        geo = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5).json()
        city = geo.get("city", "Unknown")
        country = geo.get("country", "Unknown")
        print(f"[GEO] City: {city}, Country: {country}")
    except Exception as e:
        city, country = "Unknown", "Unknown"
        print(f"[ERROR] Geolocation failed: {e}")
    open(LOG_FILE, "a").write(f"{time} | {ip} | {city}, {country} | {ua}\n")
    if os.path.exists(IMAGE_FILE):
        return send_file(IMAGE_FILE, mimetype="image/jpeg")
    else:
        return abort(404, "Image not found.")

if __name__ == '__main__':
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
