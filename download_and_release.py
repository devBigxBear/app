# coding: utf-8
import os
import requests
from datetime import datetime

# --- Configuration ---
apk_url = "https://www.dl.farsroid.com/game/Doodle-Jump-3.11.7-Mod(www.FarsRoid.com).apk"
apk_filename = f"Doodle-Jump_{datetime.now().strftime('%Y-%m-%d')}.apk"
release_tag = "daily-apk"
release_name = "Latest Doodle Jump APK"

# --- Download APK ---
print(f"Downloading APK from {apk_url}")
apk_response = requests.get(apk_url)
if apk_response.status_code != 200:
    raise Exception(f"Failed to download APK. Status code: {apk_response.status_code}")

with open(apk_filename, "wb") as f:
    f.write(apk_response.content)

# --- GitHub Release Setup ---
repo = os.environ["G]()
