import requests
from requests.auth import HTTPBasicAuth
import json
from fetch_projects import fetch_jira_projects
from jira_authentication import authentication

def create_jira_ticket(project_key, summary, description, issue_type="Bug"):
    """
    Creates a Jira ticket.

    Args:
        project_key (str): Project key (e.g., "INFRAOPS")
        summary (str): Issue summary
        description (str): Issue description
        issue_type (str, optional): Issue type (e.g., "Bug", "Task"). Defaults to "Bug".

    Returns:
        dict: Ticket creation response
    """

    auth_info = authentication()

    if not auth_info["success"]:
        return {
            "success": False,
            "error": f"Authentication failed: {auth_info['error']}"
        }

    headers = auth_info["headers"]
    auth = auth_info["auth"]
    jira_url = auth_info["jira_url"]

    url = f"{jira_url}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "issuetype": {
                "name": issue_type
            },
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            }
        }
    }

    response = requests.post(
        url,
        headers=headers,
        auth=auth,
        json=payload  # ✅ Correct usage, not data=payload
    )

    if response.status_code == 201:
        return {
            "success": True,
            "ticket": response.json()
        }
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.json() if response.text else "Unknown error"
        }

