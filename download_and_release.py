import os
import requests
from datetime import datetime

# --- Configuration ---
apk_url = "https://www.dl.farsroid.com/game/Doodle-Jump-3.11.7-Mod(www.FarsRoid.com).apk"  # Replace with the real APK URL
apk_filename = f"Doodle-Jump_{datetime.now().strftime('%Y-%m-%d')}.apk"  # Unique filename based on the current date
release_tag = datetime.now().strftime("auto-%Y-%m-%d")

# Download the APK
print(f"Downloading APK from {apk_url}")
apk_response = requests.get(apk_url)
if apk_response.status_code != 200:
    raise Exception(f"Failed to download APK. Status code: {apk_response.status_code}")

with open(apk_filename, "wb") as f:
    f.write(apk_response.content)

# Create a GitHub Release
print("Creating GitHub release...")
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}
release_data = {
    "tag_name": release_tag,
    "name": f"Auto Release {release_tag}",
    "body": "Automated APK upload.",
    "draft": False,
    "prerelease": False
}
release_response = requests.post(
    f"https://api.github.com/repos/{repo}/releases",
    headers=headers,
   

