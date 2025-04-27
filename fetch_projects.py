# This code sample uses the `requests` library
# https://docs.python-requests.org

import requests
from requests.auth import HTTPBasicAuth
import json

def fetch_jira_projects():
    # Load authentication data from auth.txt
    with open("auth.txt", "r") as file:
        auth_data = json.load(file)

    EMAIL = auth_data["email"]
    API_TOKEN = auth_data["api_token"]
    JIRA_URL = auth_data["url"]
    JIRA_ENDPOINT = "/rest/api/3/project"

    URL = f'{JIRA_URL}{JIRA_ENDPOINT}'
    AUTH = HTTPBasicAuth(EMAIL, API_TOKEN)
    print(URL)
    HEADERS = {
        "Accept": "application/json",
    }

    response = requests.request(
        "GET",
        URL,
        headers=HEADERS,
        auth=AUTH
    )
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("Connected to Jira!")
    else:
        print(f" Failed to fetch projects. Status code: {response.status_code}")


    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    output = json.loads(response.text)
    projects = []
    for project in output:
        projects.append({
            "name": project["name"],
            "id": project["id"],
            "key": project["key"]
        })

    return projects

if __name__ == "__main__":
    projects = fetch_jira_projects()