import requests
import yaml
import sys

config = yaml.safe_load(open('config.yaml'))
OWNER = config['owner']
REPO = config['repo']
TASK_ID = config['task_id']


def get_current_branches(OWNER, REPO):
    try:
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/branches"
        response = requests.get(url)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        # print(f"Response JSON: {response.json()}")
        branches = [branch['name'] for branch in response.json()]
        return branches
    except requests.RequestException as e:
        print(f"Error fetching branches: {e}")
        sys.stderr.write(f"Error fetching branches: {e}\n")
        sys.exit(1)

def expected_branches():
    expected_student = []
    for student in config['students']:
        expected_student.append(f"{TASK_ID}-{student}")
    return expected_student

def missing_branches(current, expected):
    missing = []
    for branch in expected:
        if branch not in current:
            missing.append(branch)
            print("there are missing branches")
            sys.exit(2) # Exit with code 2 if any branch is missing
        else:
            print(f" All the branches are present.")      
    return missing

print("the current branches are:", get_current_branches(OWNER, REPO))

print("the expected branches are:", expected_branches())

print("the missing branches are:", missing_branches(get_current_branches(OWNER, REPO), expected_branches()))