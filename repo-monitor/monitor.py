import requests
import sys
import yaml
#1
OWNER = "Ferrum-Axion"
REPO_NAME = "python-projects"

response = requests.get(f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches")
print (response.json())
print (response.status_code)
#2
data = response.json()
names_lambda=list(map(lambda b : b["name"], data))
names_list_comp = [branch["name"] for branch in data]

print (names_list_comp)
print (names_lambda)
#3
TASK_ID = "repo-monitor"
import requests

try:
    response = requests.get(f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches",timeout=10)
    response.raise_for_status()  
    data = response.json()
except requests.exceptions.Timeout as e:
    print(f"Failure: The request timed out: {e}", file=sys.stderr)
    sys.exit(1) 
except requests.exceptions.HTTPError as e:
    print(f"Failure: HTTP error: {e}", file=sys.stderr)
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"Failure: A general request error occurred: {e}", file=sys.stderr)
    sys.exit(1)
else:
    print (f"Success",names_lambda)
#4
expected_students = ['liad','aviv','dmitry','dvir','elena','gal','yaron','rafi','mattan','vladi']
expected_branch_names = [f"{TASK_ID}-{student}" for student in expected_students]
did_not_submit = set(expected_branch_names) - set(names_list_comp)
if did_not_submit:
    print (f"Missing branches:{did_not_submit}")
    sys.exit(2)
else:
    print ("Everyone submitted")
    sys.exit(0)
#5 - clean version + using yaml file
with open(config.yaml):
 config = {config.yaml}
try:
    response = requests.get(f"https://api.github.com/repos/{config["OWNER"]}/{config["REPO_NAME"]}/branches",timeout=10)
    response.raise_for_status()  
    data = response.json()
except requests.exceptions.Timeout as e:
    print(f"Failure: The request timed out: {e}", file=sys.stderr)
    sys.exit(1) 
except requests.exceptions.HTTPError as e:
    print(f"Failure: HTTP error: {e}", file=sys.stderr)
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"Failure: A general request error occurred: {e}", file=sys.stderr)
    sys.exit(1)
else:
    print (f"Success")
expected_students = [config["students"]]
expected_branch_names = [f"{TASK_ID}-{student}" for student in expected_students]
did_not_submit = set(expected_branch_names) - set(names_list_comp)
if did_not_submit:
    print (f"Missing branches:{did_not_submit}")
    sys.exit(2)
else:
    print ("Everyone submitted")
    sys.exit(0)

