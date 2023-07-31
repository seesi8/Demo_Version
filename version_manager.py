import requests
import time

# Replace 'YOUR_API_KEY' with your actual GitHub personal access token
API_KEY = "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"


def get_latest_release(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    if API_KEY:
        headers = {"Authorization": f"token {API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        releases = response.json()
        # Sort releases based on the published date, with the latest first
        releases.sort(key=lambda r: r["published_at"], reverse=True)
        for release in releases:
            if not release["prerelease"]:
                return release["tag_name"]
    return None


def version_manage():
    while True:
        if not API_KEY:
            time.sleep(100)
        else:
            time.sleep(1)
        latest_release = get_latest_release("seesi8", "ballbert")
        if latest_release:
            print(f"Latest release: {latest_release}")
        else:
            print("Unable to retrieve the latest release.")


version_manage()
