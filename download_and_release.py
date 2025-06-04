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
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["MY_GITHUB_PAT"]  # ✅ CHANGED from GITHUB_TOKEN to your custom token
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# --- Check if release already exists ---
release_api_url = f"https://api.github.com/repos/{repo}/releases/tags/{release_tag}"
release_response = requests.get(release_api_url, headers=headers)

if release_response.status_code == 200:
    # Release exists
    release = release_response.json()
    release_id = release["id"]
    upload_url = release["upload_url"].split("{")[0]

    # Delete any existing asset with the same name
    print("Checking existing assets...")
    for asset in release["assets"]:
        if asset["name"] == apk_filename:
            print(f"Deleting existing asset: {apk_filename}")
            delete_url = asset["url"]
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code != 204:
                raise Exception("Failed to delete existing asset")
else:
    # Create a new release
    print("Creating a new GitHub release...")
    release_data = {
        "tag_name": release_tag,
        "name": release_name,
        "body": "Automated APK upload (daily).",
        "draft": False,
        "prerelease": False
    }
    create_release_response = requests.post(
        f"https://api.github.com/repos/{repo}/releases",
        headers=headers,
        json=release_data
    )
    if create_release_response.status_code != 201:
        print("Error creating release:", create_release_response.text)
        raise Exception("Failed to create release")
    release = create_release_response.json()
    upload_url = release["upload_url"].split("{")[0]

# --- Upload the APK file ---
print("Uploading APK...")
with open(apk_filename, "rb") as f:
    apk_data = f.read()

upload_headers = dict(headers)
upload_headers["Content-Type"] = "application/vnd.android.package-archive"

upload_response = requests.post(
    f"{upload_url}?name={apk_filename}",
    headers=upload_headers,
    data=apk_data
)

if upload_response.status_code != 201:
    print("Error uploading APK:", upload_response.text)
    raise Exception("Failed to upload APK")

print("✅ APK uploaded successfully!")
