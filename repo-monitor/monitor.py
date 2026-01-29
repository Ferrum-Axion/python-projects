import requests
import sys
#1
OWNER = "Ferrum-Axion"
REPO_NAME = "python-projects"

response=requests.get(f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches")
print (response.json())
print (response.status_code)
#2

