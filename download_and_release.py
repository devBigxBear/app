import os
import requests
from datetime import datetime

# Get environment variables securely provided by GitHub Actions
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "devBigxBear/app")
APK_URL = "https://www.dl.farsroid.com/game/Doodle-Jump-3.11.7-Mod(www.FarsRoid.com).apk"

def generate_unique_tag():
    # Example: release-2025-06-04-12-31-50
    return "release-" + datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")

def create_release(tag_name):
    api_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "tag_name": tag_name,
        "name": tag_name,
        "body": "Automated APK release",
        "draft": False,
        "prerelease": False
    }
    resp = requests.post(api_url, json=data, headers=headers)
    if resp.status_code == 201:
        return resp.json()["upload_url"].split("{")[0], resp.json()["id"]
    elif resp.status_code == 422 and any(e.get("code") == "already_exists" for e in resp.json().get("errors", [])):
        raise Exception(f"Release with tag '{tag_name}' already exists. Please use a unique tag.")
    else:
        raise Exception(f"Failed to create release: {resp.text}")

def upload_asset(upload_url, file_path):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/vnd.android.package-archive"
    }
    params = {"name": os.path.basename(file_path)}
    with open(file_path, "rb") as f:
        resp = requests.post(upload_url, headers=headers, params=params, data=f)
    if resp.status_code not in (201, 200):
        raise Exception(f"Failed to upload asset: {resp.text}")

def main():
    # Download APK
    apk_file_path = "latest.apk"
    apk_response = requests.get(APK_URL)
    apk_response.raise_for_status()
    with open(apk_file_path, "wb") as apk_file:
        apk_file.write(apk_response.content)

    # Create release with unique tag
    tag_name = generate_unique_tag()
    upload_url, _ = create_release(tag_name)

    # Upload APK to release
    upload_asset(upload_url, apk_file_path)
    print(f"Release created and APK uploaded with tag: {tag_name}")

if __name__ == "__main__":
    main()
