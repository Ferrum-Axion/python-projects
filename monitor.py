import requests
import sys

OWNER = "Ferrum-Axion"
REPO_NAME = "python-projects"
url = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches"

try:
    response = requests.get(url, timeout=10)
    
    if response.status_code == 404:
        print(f"Error: Repository {OWNER}/{REPO_NAME} not found.", file=sys.stderr)
        sys.exit(1)
    elif response.status_code == 401:
        print("Error: Unauthorized. Check your access rights.", file=sys.stderr)
        sys.exit(1)
    elif response.status_code != 200:
        print(f"Error: GitHub API returned status {response.status_code}", file=sys.stderr)
        sys.exit(1)

    branches_data = response.json()
    names_list = [b["name"] for b in branches_data]
    
    print("Success! Branch names:")
    for name in names_list:
        print(f"- {name}")

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the internet.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)