from datetime import datetime
import os
import platform
import shutil
import requests
import time
import subprocess

# Replace 'YOUR_API_KEY' with your actual GitHub personal access token
API_KEY = open("./Demo_Version/key").read()


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


def run_update(current_version, latest_release):
    def clone_specific_version(repo_url, version, destination):
        """
        Clone a specific version of a Git repository.

        Args:
            repo_url (str): URL of the Git repository.
            version (str): The specific version or commit hash to clone.
            destination (str): The path where the repository will be cloned.

        Returns:
            bool: True if cloning was successful, False otherwise.
        """
        try:
            # Run the git clone command
            subprocess.run(["git", "clone", repo_url, destination], check=True)

            # Change the working directory to the cloned repository
            working_dir = f"{destination.rstrip('/')}/.git"
            subprocess.run(["git", "checkout", version], cwd=working_dir, check=True)

            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return False

    def run_update_script(destination):
        """
        Clone a specific version of a Git repository.

        Args:
            repo_url (str): URL of the Git repository.
            version (str): The specific version or commit hash to clone.
            destination (str): The path where the repository will be cloned.

        Returns:
            bool: True if cloning was successful, False otherwise.
        """
        try:
            # Run the git clone command
            subprocess.run(["sudo", f"{destination}/update.sh"], check=True)

            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return False

    # Example usage
    repo_url = "https://github.com/seesi8/Demo_Version.git"
    version_to_clone = latest_release  # Replace with the specific version or commit hash you want to clone
    destination_path = "C:\\Users\\samue\\OneDrive\\Documents\\Demo_Version"

    if clone_specific_version(repo_url, version_to_clone, destination_path):
        return run_update_script(destination=destination_path)
    else:
        return False


def update_version(current_release, latest_release):
    if platform.system() == "Linux":
        backupdir = "/etc/ballbert/backups"
    else:
        backupdir = "A:/test/backups"

    if not os.path.exists(backupdir):
        os.makedirs(backupdir)

    hour = datetime.now().hour

    hour = 3
    if hour >= 2 and hour <= 3:
        shutil.copytree("./Demo_Version", os.path.join(backupdir, latest_release))
        os.system(f"python {backupdir}/{latest_release}/run_update.py")
        while True:
            pass
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
            with open("./Demo_Version/CURRENT_VERSION", "r") as file:
                current_release = file.read()

            print(latest_release, current_release)

            if latest_release == current_release:
                print("up to date")
            else:
                if update_version(current_release, latest_release):
                    with open("./Demo_Version/CURRENT_VERSION", "w") as file:
                        file.write(latest_release)

        else:
            print("Unable to retrieve the latest release.")


version_manage()
