import requests
import sys
import yaml
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient  
from sendgrid.helpers.mail import Mail  

load_dotenv()

SENDGRID_API_KEY_ELENA = os.getenv("SENDGRID_API_KEY_ELENA")

def send_email(subject, body):
    api_key=os.getenv("SENDGRID_API_KEY_ELENA")
    message = Mail(
        from_email="elena.kyurshunova@gmail.com",
        to_emails="elena.kyrushunova@gmail.com",
        subject=subject,
        plain_text_content=body
    )
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)

try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config.yaml not found", file=sys.stderr)
    sys.exit(1)

OWNER = config["owner"]
REPO_NAME = config["repo"]
TASK_NAME = config["task_id"]
expected_students = config["students"]

url = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches"

try:
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        print(f"Error: Repository {OWNER}/{REPO_NAME} not found", file=sys.stderr)
        sys.exit(1)
    elif response.status_code == 401:
        print("Error: Unauthorized access", file=sys.stderr)
        sys.exit(1)
    elif response.status_code != 200:
        print(f"Error: API returned status {response.status_code}", file=sys.stderr)
        sys.exit(1)

    actual_branches = [b["name"] for b in response.json()]
    
    expected_branches = [f"{TASK_NAME}-{student}" for student in expected_students]
    
    missing_submissions = set(expected_branches) - set(actual_branches)

    print("--- Results ---")
    if missing_submissions:
        print("Missing branches:")
        for missing in sorted(missing_submissions):
            print(f"  [MISSING] {missing}")
        sys.exit(2)
    else:
        print("Success: All students submitted their branches!")
        subject_text = f"Repo Monitor: {TASK_NAME} - Success!"
        body_text = f"Yay, all students have succesfully submited their branches to {REPO_NAME}!"

        send_email(subject_text, body_text)

        sys.exit(0)

except requests.exceptions.ConnectionError:
    print("Error: No internet connection", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)