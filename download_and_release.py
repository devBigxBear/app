import os
import requests
from datetime import datetime

# 1️⃣ Configuration
apk_url = "https://www.dl.farsroid.com/ap/Bluelight-Filter-Unlocked-6.3.4(www.FarsRoid.com).apk"  # 🔁 Replace this with the actual APK URL
apk_filename = "downloaded_app.apk"
release_tag = datetime.now().strftime("auto-%Y-%m-%d")

# 2️⃣ Download the APK
print(f"Downloading APK from {apk_url}")
apk_response = requests.get(apk_url)
if apk_response.status_code != 200:
    raise Exception(f"Failed to download APK. Status code: {apk_response.status_code}")

with open(apk_filename, "wb") as f:
    f.write(apk_response.content)

# 3️⃣ Create a GitHub Release
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
    json=release_data
)
if release_response.status_code != 201:
    print("Error creating release:", release_response.text)
    raise Exception("Failed to create release")

release = release_response.json()
upload_url = release["upload_url"].split("{")[0]

# 4️⃣ Upload APK to the release
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
