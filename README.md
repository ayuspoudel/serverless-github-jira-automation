
# Serverless GitHub → Jira Automation

This project is a Python-based serverless API that automates the creation of Jira tickets from GitHub issues. When authorized users comment `/jira` on an issue, a corresponding Jira ticket is created with relevant metadata and context. This saves time and streamlines your workflow.

## Features

- Authenticated comment-based trigger (`/jira`)
- GitHub issue to Jira ticket sync
- Automatic triage logic based on labels and issue content
- Modular structure for easy extension

## Project Structure

src/
- automated_triage.py         - Logic to prioritize and route tickets
- create_ticket.py            - Jira ticket creation and field mapping
- fetch_projects.py           - Fetch available Jira projects and types
- issuetypes.py               - Maps issue types and project keys
- jira_authentication.py      - OAuth or API token-based Jira auth

## How It Works

1. A user comments `/jira` on a GitHub issue
2. The serverless API:
   - Verifies the user is authorized
   - Extracts issue title, description, and labels
   - Determines the target project and issue type
   - Creates a Jira ticket using the Jira API
3. The ticket ID is posted as a comment on the original GitHub issue

## Requirements

- Python 3.9+
- Jira Cloud account with API token
- GitHub repository with webhook/event listener

requirements.txt:
```

requests
fastapi
uvicorn
python-dotenv

````

## Security

- Uses environment variables and token-based authentication
- Can be extended with HMAC signature checks from GitHub webhooks

## Deployment Options

- AWS Lambda with API Gateway
- Docker container (Dockerfile provided)
- Serverless Framework or Terraform

## Example Request

POST /github-event-webhook

```json
{
  "action": "created",
  "comment": {
    "body": "/jira",
    "user": {
      "login": "authorized-contributor"
    }
  },
  "issue": {
    "title": "Login button not working",
    "body": "Steps to reproduce...",
    "labels": ["bug", "frontend"]
  }
}
````

## Contributors

Ayush Poudel ([https://github.com/ayuspoudel](https://github.com/ayuspoudel))

## Future Enhancements

* Slack notifications on ticket creation
* Auto-assign based on GitHub assignee
* Error logging and observability with Prometheus

