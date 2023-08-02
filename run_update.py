from datetime import datetime
import os
import platform
import re
import shutil
import requests
import time
import subprocess

# Replace 'YOUR_API_KEY' with your actual GitHub personal access token
API_KEY = open("./Demo_Version/key").read()


def rmtree_hard(path, _prev=""):
    try:
        shutil.rmtree(path)
    except PermissionError as e:
        if e == _prev:
            return
        match = re.search(r"Access is denied: '(.*)'", str(e))
        if match:
            file_path = match.group(1)
            os.chmod(file_path, 0o777)

            # Delete the file
            os.remove(file_path)
            rmtree_hard(path, _prev=e)
        else:
            raise e


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
            subprocess.run(
                ["git", "clone", "--branch", latest_release, repo_url, destination],
                check=True,
            )

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

    rmtree_hard("C:\\Users\\samue\\OneDrive\\Documents\\Demo_Version")
    # Example usage
    repo_url = "https://github.com/seesi8/Demo_Version.git"
    version_to_clone = latest_release  # Replace with the specific version or commit hash you want to clone
    destination_path = "C:\\Users\\samue\\OneDrive\\Documents\\Demo_Version"

    if clone_specific_version(repo_url, version_to_clone, destination_path):
        return run_update_script(destination=destination_path)
    else:
        return False


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


with open("./Demo_Version/CURRENT_VERSION", "r") as file:
    current_release = file.read()
run_update(current_release, get_latest_release("seesi8", "Demo_Version"))
