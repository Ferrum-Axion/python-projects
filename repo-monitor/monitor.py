import requests
import sys

OWNER = "Ferrum-Axion"
REPO = "python-projects"

def get_branches():
    try:
        response =requests.get(f"https://api.github.com/repos/{OWNER}/{REPO}/branches")
        data = response.json()
        branches_names = list(map(lambda b : b["name"], data))
        print(branches_names)
    except requests.exceptions.HTTPError as errh:
        sys.stderr.write(str(errh))
        sys.exit(1)

get_branches()