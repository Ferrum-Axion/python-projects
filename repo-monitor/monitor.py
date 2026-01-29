import requests
import yaml
import sys


config = None
def get_config():
    global config
    if config is None:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
    return config

def get_branches_names():
    cfg = get_config()
    try:
        response = requests.get(f"https://api.github.com/repos/{cfg['owner']}/{cfg['repo']}/branches")
        response.raise_for_status()
        names = list(map(lambda x: x['name'], response.json()))
        return names
    except requests.exceptions.HTTPError as e:
        print("HTTP error: " + e, file=sys.stderr)
        sys.exit(1)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
        print("Connection error: " + e, file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print("Error incomplete config.yaml: " + e, file=sys.stderr)
        sys.exit(1)

def get_expected_branches():
    cfg = get_config()
    try:
        return list(map(lambda x: cfg['task_id'] + '-' + x, cfg['students']))
    except KeyError as e:
        print("Error incomplete config.yaml: " + e, file=sys.stderr)
        sys.exit(1)

def check_submittions(branch_names, expected_branches):
    not_submitted = []
    for e in expected_branches:
        if e not in branch_names:
            not_submitted.append(e)
    return not_submitted

def print_out(not_submitted):
    if len(not_submitted) == 0:
        print("Everyone submitted the task")
    else:
        print("Not submitted branches: " + str(not_submitted))

if '__main__' == __name__:
    # print(get_branches_names())
    # print(get_expected_branches())
    not_sub = check_submittions(get_branches_names(), get_expected_branches())
    print_out(not_sub)
