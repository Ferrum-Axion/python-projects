import requests

OWNER = "Ferrum-Axion"
REPO_NAME = "python-projects"

url = f"https://api.github.com/repos/Ferrum-Axion/python-projects/branches"

response = requests.get(url)

print("Status code:", response.status_code)
print("Raw JSON response:")
print(response.json())
