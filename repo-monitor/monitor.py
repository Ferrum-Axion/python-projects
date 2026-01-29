import requests
import sys

REPO = "python-projects"
OWNER = "Ferrum-Axion"

def get_branches():
    try:
        response = requests.get(f"https://api.github.com/repos/{OWNER}/{REPO}/branches")
        response.raise_for_status()
        data = response.json()
        if response.status_code != 200:
            raise
        branches_name = list(map(lambda b : b["name"], data))
        print(branches_name)
    except requests.exceptions.HTTPError as errh:
        print("error is: ",errh)

get_branches()