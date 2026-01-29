import requests
import sys
import os
import yaml

#REPO = "python-projects"
#OWNER = "Ferrum-Axion"

def configfiledata():
    with open("./config.yaml") as file:
        return yaml.safe_load(file)



def get_branches():
    config = configfiledata()
    try:
        response = requests.get(f"https://api.github.com/repos/{config["owner"]}/{config["repo"]}/branches")
        response.raise_for_status()
        data = response.json()
        if response.status_code != 200:
            raise
        branches_name = list(map(lambda b : b["name"], data))
        print(branches_name)
    except requests.exceptions.HTTPError as errh:
        print("error is: ",errh)

get_branches()