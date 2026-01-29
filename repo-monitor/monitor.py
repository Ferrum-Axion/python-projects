

from typing import Any


import requests

OWNER = "Ferrum-Axion"
REPO_NAME = "python-projects"

BRANCHES_URL = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches"


def main():
    try:
        response = requests.get(BRANCHES_URL)
        response.raise_for_status()
        branches = response.json()

        branch_names_comprehension = [b["name"] for b in branches]
        branch_names_map = list(map(lambda b: b["name"], branches))
        branch_names = branch_names_comprehension
        for name in branch_names:
            print(name)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except (ValueError, KeyError) as e:
        print(f"Invalid response: {e}")


if __name__ == "__main__":
    main()
