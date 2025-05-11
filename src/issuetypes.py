import requests
from requests.auth import HTTPBasicAuth
import json
import sys

# Load auth
with open("auth.txt", "r") as file:
    auth_data = json.load(file)

email = auth_data["email"]
api_token = auth_data["api_token"]
jira_url = auth_data["url"]

# Setup authentication
auth = HTTPBasicAuth(email, api_token)

# 1️⃣ Get GitHub repo name dynamically
# (either passed as command line argument or set manually for now)
if len(sys.argv) != 2:
    print("Usage: python3 script.py <github_repo_name>")
    sys.exit(1)

repo_name = sys.argv[1]  # Example: serverless-github-jira-automation

# 2️⃣ Find the matching Jira project based on repo_name

# URL to search all projects
search_url = f"{jira_url}/rest/api/3/project/search"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Fetch all projects
response = requests.get(search_url, headers=headers, auth=auth)

if response.status_code != 200:
    print(f"Failed to fetch projects. Status: {response.status_code}")
    print(response.text)
    sys.exit(1)

projects = response.json().get('values', [])

# Try to find the project whose name matches the repo_name
matching_project = None
for project in projects:
    if project['name'].lower() == repo_name.lower() or project['key'].lower() == repo_name.lower():
        matching_project = project
        break

if not matching_project:
    print(f"No matching project found for repo name: {repo_name}")
    sys.exit(1)

project_id = matching_project['id']
project_name = matching_project['name']
project_key = matching_project['key']

print(f"✅ Matched project: {project_name} (Key: {project_key}, ID: {project_id})")

# 3️⃣ Now fetch the issue types for that project

issuetype_url = f"{jira_url}/rest/api/3/issuetype/project"

params = {
    "projectId": project_id
}

response = requests.get(issuetype_url, headers=headers, auth=auth, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"\n📋 Issue types for project '{project_name}':\n")
    for issue_type in data.get('issueTypes', []):
        print(f"Name: {issue_type['name']} | ID: {issue_type['id']}")
else:
    print(f"Failed to fetch issue types. Status: {response.status_code}")
    print(response.text)
