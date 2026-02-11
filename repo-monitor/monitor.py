import requests
import yaml
import sys
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

        # Send notification email 
        load_dotenv()

        def send_email(subject, body):
            api_key = os.getenv("SENDGRID_API_KEY")
            sender = os.getenv("SENDER_EMAIL")
            recipient = os.getenv("RECIPIENT_EMAIL")
            if not api_key or not sender or not recipient:
                print("Warning: Email not sent, missing environment variables", file=sys.stderr)
                return
            subject = f"Repo Monitor: {subject}"
            message = Mail(from_email=sender, to_emails=recipient, subject=subject, html_content=body)
            try:
                sg = SendGridAPIClient(api_key)
                sg.send(message)
                print("Notification email sent.")
                return True
            except Exception as e:
                print(f"Error: Failed to send email — {e}", file=sys.stderr)
                return False
            
        # Build email content and send
        subject = f"All submissions received for {task_name}"
        body = "<p>All expected branches were found:</p><ul>"
        for name in sorted(expected_branches):
            body += f"<li>{name}</li>"
        body += "</ul>"

        send_email(subject, body)
        sys.exit(0)
        
except requests.RequestException as e:
    print(f"Error: Network request failed — {e}", file=sys.stderr)
    sys.exit(1)