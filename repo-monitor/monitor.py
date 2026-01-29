import requests
import sys
import os
import yaml


def configfiledata():
    with open("./config.yaml") as file:
        return yaml.safe_load(file)


def checksubmitted(expected_branches, expected_students):
    not_submitted = []
    for s in expected_students:
        if s.lower() not in expected_branches:
            not_submitted.append(s.lower())
    return not_submitted    


def get_branches():
    config = configfiledata()
    taskid = config["task_id"]

    try:
        response = requests.get(f"https://api.github.com/repos/{config["owner"]}/{config["repo"]}/branches")
        response.raise_for_status()
        data = response.json()
        branches_exists = list(map(lambda b : b["name"].lower(), data))
        branches_expected = list(map(lambda s : f"{taskid}-{s}", config["students"]))
        missing_subbmissions = checksubmitted(branches_exists, branches_expected)
        if len(missing_subbmissions) == 0:
            print("All student submitted the projects")
        else:
            print(f"These students did not submitted: {str(missing_subbmissions)}")
  #      if response.status_code != 200:
  #          raise

    except requests.exceptions.HTTPError as errh:
        print("error is: ",errh)

get_branches()