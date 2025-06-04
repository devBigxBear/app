import requests
import os
import datetime
import sys

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
APK_URL = "https://www.dl.farsroid.com/game/Doodle-Jump-3.11.7-Mod(www.FarsRoid.com).apk"
APK_FILENAME = "Doodle-Jump.apk"

if not GITHUB_TOKEN or not GITHUB_REPOSITORY:
    print("Missing GITHUB_TOKEN or GITHUB_REPOSITORY environment variable.")
    sys.exit(1)

# Download APK file
def download_apk(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {filename}")

# Generate a unique tag name using current datetime
def get_unique_tag():
    now = datetime.datetime.utcnow()
    return f"release-{now.strftime('%Y%m%d-%H%M%S')}"

def create_github_release(tag_name, token, repo):
    api_url = f"https://api.github.com/repos/{repo}/releases"
    release_data = {
        "tag_name": tag_name,
        "name": f"Automated APK Release {tag_name}",
        "body": "Automated upload of APK file.",
        "draft": False,
        "prerelease": False
    }
    headers = {"Authorization": f"token {token}"}
    response = requests.post(api_url, json=release_data, headers=headers)
    if response.status_code == 201:
        print(f"Release created: {response

