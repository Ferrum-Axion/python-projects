import os
import sys
from pathlib import Path

import requests
import yaml
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def send_mail(subject, body):
    """Send email via SendGrid using SENDGRID_API_KEY_Tomer and SENDGRID_SENDER_EMAIL_Tomer from env."""
    api_key = os.environ.get("SENDGRID_API_KEY_Tomer")
    sender = os.environ.get("SENDGRID_SENDER_EMAIL_Tomer")
    if not api_key or not sender:
        return  # skip if secrets not set (e.g. local run without .env)
    message = Mail(
        from_email=sender,
        to_emails=sender,
        subject=subject,
        html_content=f"<strong>{body}</strong>",
    )
    client = SendGridAPIClient(api_key)
    client.send(message)


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    try:
        config = load_config()
    except (OSError, yaml.YAMLError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)

    owner = config["owner"]
    repo = config["repo"]
    task_id = config["task_id"]
    students = config["students"]

    branches_url = f"https://api.github.com/repos/{owner}/{repo}/branches"

    try:
        response = requests.get(branches_url)
        response.raise_for_status()
        branches = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, KeyError) as e:
        print(f"Invalid response: {e}", file=sys.stderr)
        sys.exit(1)

    # {task_id}-{student}
    expected_branches = [f"{task_id}-{student}" for student in students]
    actual_branches = [b["name"] for b in branches]

    missing = set(expected_branches) - set(actual_branches)

    if missing:
        print("Missing submissions:")
        for name in sorted(missing):
            print(name)
        sys.exit(2)

    print("All expected submissions are present.")
    send_mail("Repo monitor: all submissions in", "All students submitted.")
    sys.exit(0)


if __name__ == "__main__":
    main()
