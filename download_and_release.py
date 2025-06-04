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

# Prepare GitHub API
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Get or create release
release_check_url = f"https://api.github.com/repos/{repo}/releases/tags/{release_tag}"
release_response = requests.get(release_check_url, headers=headers)
if release_response.status_code == 200:
    print(f"Release with tag {release_tag} found, updating it.")
    release = release_response.json()
else:
    print(f"Release with tag {release_tag} not found, creating new release.")
    release_data = {
        "tag_name": release_tag,
        "name": f"Auto Release {release_tag}",
        "body": "Automated APK upload.",
        "draft": False,
        "prerelease": False
    }
    release_create_response = requests.post(
        f"https://api.github.com/repos/{repo}/releases",
        headers=headers,
        json=release_data
    )
    if release_create_response.status_code != 201:
        print("Error creating release:", release_create_response.text)
        raise Exception("Failed to create release")
    release = release_create_response.json()

upload_url = release["upload_url"].split("{")[0]

# Delete asset with the same name if exists
assets_url = release["assets_url"]
assets_response = requests.get(assets_url, headers=headers)
if assets_response.status_code == 200:
    assets = assets_response.json()
    for asset in assets:
        if asset["name"] == apk_filename:
            print(f"Deleting existing asset {apk_filename}...")
            delete_url = asset["url"]
            del_response = requests.delete(delete_url, headers=headers)
            if del_response.status_code != 204:
                print("Failed to delete existing asset:", del_response.text)
            else:
                print("Existing asset deleted.")

# Upload APK to the release
print("Uploading APK to release...")
with open(apk_filename, "rb") as f:
    apk_data = f.read()

upload_response = requests.post(
    f"{upload_url}?name={apk_filename}",
    headers={**headers, "Content-Type": "application/vnd.android.package-archive"},
    data=apk_data
)
if upload_response.status_code != 201:
    print("Error uploading APK:", upload_response.text)
    raise Exception("Failed to upload APK")

print("✅ Done! APK uploaded successfully.")
