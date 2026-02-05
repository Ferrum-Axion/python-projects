
import requests
import sys
import yaml
from dotenv import load_dotenv
import os
import certifi
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()

print(certifi.where())

def get_config():
    with open("./config.yaml") as file:
        return yaml.safe_load(file)

def students_all_submitted(branches, expected_students):
    not_submitted = []
    is_all_submitted= True
    for s in expected_students:
        if s.lower() not in branches:
            not_submitted.append(s.lower())
            is_all_submitted =False
    return is_all_submitted, not_submitted

def open_issue(not_submitted_names):
    try:
        config = get_config()
        token = os.environ.get("GH_TOKEN")
        headers = {"Authorization" : f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version":"2022-11-28"}
        body = {"title": "missing submissions", "body": str(not_submitted_names)}
        
        response = requests.post(f"https://api.github.com/repos/{config['owner']}/{config['repo']}/issues",headers=headers, json=body)
        print(token)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(str(errh))



def send_mail(subject, body):
    email_from = os.environ["EMAIL_ADDRESS_NAHAR"]
    api_key = os.environ["SENDGRID_API_KEY"]

    message = Mail(from_email=email_from, to_emails= email_from, 
                   subject=subject, html_content=f"<strong>{body}</strong>")
    sendgrid_client = SendGridAPIClient(api_key)
    response = sendgrid_client.send(message)
    print(response.status_code)



def get_branches():
        config = get_config()
        task_id = config["task_id"]
        try:
            
            response = requests.get(f"https://api.github.com/repos/{config['owner']}/{config['repo']}/branches")
            response.raise_for_status()

            
            data = response.json()
            
            branches_names = list(map(lambda b : b["name"].lower(), data))

            expected_branches = list(map(lambda s : f"{task_id}-{s}" , config['students']))
            all_submitted,not_submitted_names = students_all_submitted(branches_names, expected_branches)
            print(not_submitted_names)
            if all_submitted:
                send_mail("sendgrid test","All student submited!")
                sys.stdout.write("All studentes submited the homework")
            else:
                send_mail("theese didint submit yet",' '.join(not_submitted_names))
                # open_issue(not_submitted_names)

        except requests.exceptions.HTTPError as errh:
            sys.stderr.write(str(errh))
            sys.exit(1)





# def send_email_gmail(subject: str, body: str):

#     sender = os.getenv("EMAIL_ADDRESS")
#     password = os.getenv("EMAIL_PASSWORD")
#     print(password)
#     message = MIMEMultipart()
#     message["From"] = sender
#     message["To"]  = sender
#     message["Subject"] = "This is a test subject"

#     message.attach(MIMEText(body,"plain"))
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(sender,password)
#     server.sendmail(sender,sender, message.as_string())
#     server.quit()

get_branches()
