import sys
import requests

OWNER = "Ferrum-Axion"
REPO_NAME = "python-projects"

TASK_NAME = "repo-monitor"  # זה ה-TASK_ID/שם המשימה
expected_students = [
    "rafi",
    "yaron",
    "vladi",
    "tomer",
    "liad",
    "elena",
    "dvir",
    "dmitry",
    "aviv",
]

url = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches"

# -------------------------
# Step 3: error handling
# -------------------------
try:
    response = requests.get(url, timeout=15)
except requests.exceptions.RequestException as e:
    print("ERROR: Network/Request problem while contacting GitHub API")
    print("Details:", e)
    sys.exit(1)

print("Status code:", response.status_code)

if response.status_code != 200:
    print("ERROR: GitHub API returned a non-200 response")
    print("Response text:", response.text)
    sys.exit(1)

try:
    branches = response.json()
except ValueError:
    print("ERROR: Response is not valid JSON")
    print("Response text:", response.text)
    sys.exit(1)

if not isinstance(branches, list):
    print("ERROR: Expected a list of branch objects, got:", type(branches))
    print("Raw JSON response:")
    print(branches)
    sys.exit(1)

# -------------------------
# Step 2: extract names
# -------------------------
actual_branches = [b["name"] for b in branches]

print("\nActual branch names:")
print(actual_branches)

# -------------------------
# Step 4: expected branches
# -------------------------
expected_branches = [f"{TASK_NAME}-{student}" for student in expected_students]

print("\nExpected branch names:")
print(expected_branches)

# Compare (set difference)
missing = sorted(list(set(expected_branches) - set(actual_branches)))

print("\n=== RESULT ===")
if missing:
    print("Missing submissions (branches not found):")
    for b in missing:
        print("-", b)
    sys.exit(2)
else:
    print("✅ All submissions found. Great job!")
    sys.exit(0)
