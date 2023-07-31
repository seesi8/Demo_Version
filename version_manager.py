from datetime import datetime
import requests
import time

# Replace 'YOUR_API_KEY' with your actual GitHub personal access token
API_KEY = open("key").read()


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


def update_version():
    hour = datetime.now().hour

    hour = 3
    if hour >= 2 and hour <= 3:
        print("updating")

    else:
        print("Wrong time")
        return False


def version_manage():
    while True:
        if not API_KEY:
            time.sleep(100)
        else:
            time.sleep(1)
        latest_release = get_latest_release("seesi8", "Demo_Version")
        if latest_release:
            with open("CURRENT_VERSION", "r") as file:
                current_release = file.read()

            print(latest_release, current_release)

            if latest_release == current_release:
                print("up to date")
            else:
                if update_version():
                    with open("CURRENT_VERSION", "w") as file:
                        file.write(latest_release)

        else:
            print("Unable to retrieve the latest release.")


version_manage()
