import requests
import sys
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

owner = config["owner"]
repo = config["repo"]
task_name = config["task_id"]
expected_students = config["students"]

url = f"https://api.github.com/repos/{owner}/{repo}/branches"

try:
    response = requests.get(url)
    if response.status_code == 404:
        print("Error: Repository not found.", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 401:
        print("Error: Unauthorized.", file=sys.stderr)
        sys.exit(1)
    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}.", file=sys.stderr)
        sys.exit(1)

    branches = response.json()
    actual_branches = [b["name"] for b in branches]
    expected_branches = [f"{task_name}-{s.strip()}" for s in expected_students]
    missing = set(expected_branches) - set(actual_branches)

    if missing:
        print("Missing:")
        for name in sorted(missing):
            print("  -", name)
        sys.exit(2)
    else:
        print("All submitted.")
        sys.exit(0)

except requests.RequestException as e:
    print(f"Error: Network request failed — {e}", file=sys.stderr)
    sys.exit(1)