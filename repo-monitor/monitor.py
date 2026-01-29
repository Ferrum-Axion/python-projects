

import requests

OWNER = "Ferrum-Axion"
REPO_NAME = "python-projects"

BRANCHES_URL = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches"


def main():
    try:
        response = requests.get(BRANCHES_URL)
        response.raise_for_status()
        branches = response.json()
        for branch in branches:
            print(f"branches in repo: {REPO_NAME}")
            print(branch["name"])
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except (ValueError, KeyError) as e:
        print(f"Invalid response: {e}")


if __name__ == "__main__":
    main()
