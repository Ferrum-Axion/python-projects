import requests
import yaml
import sys
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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

def missing_branches (branches, expected_student):
    missing = []
    for branch in expected_student:
        if branch not in branches:
            missing.append(branch)
            # sys.exit(2) # Exit with code 2 if any branch is missing
    return missing

def send_email(missing):
    email_from = os.getenv('EMAIL_ADDRESS_LIAD')
    api_key = os.getenv('SENDGRID_API_KEY_LIAD')
    message = Mail(
        from_email=email_from, 
        to_emails=email_from,
        subject='Missing Branches Alert',
        html_content=f"<strong>Missing branches: {missing}</strong>")
    sendgrid_client = SendGridAPIClient(api_key)
    response = sendgrid_client.send(message)
    print(response.status_code)


def main():
    branches = get_current_branches(OWNER, REPO)
    expected_student = expected_branches()
    missing = missing_branches(branches, expected_student)
    print(missing)
    if missing:
        print("Missing branches:", missing)
    else:
        print("All branches are present.")
        send_email(missing)

if __name__ == "__main__":
    main()
