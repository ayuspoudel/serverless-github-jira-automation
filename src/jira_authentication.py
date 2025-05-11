import json
from requests.auth import HTTPBasicAuth

def authentication():
    """
    Authenticates to Jira and returns authentication info as a JSON-style dictionary.

    Returns:
        dict: A dictionary with keys 'headers', 'auth', and 'jira_url'
    """

    try:
        with open("auth.txt", "r") as file:
            auth_data = json.load(file)

        email = auth_data["email"]
        api_token = auth_data["api_token"]
        jira_url = auth_data["url"]

        auth = HTTPBasicAuth(email, api_token)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        return {
            "success": True,
            "headers": headers,
            "auth": auth,
            "jira_url": jira_url
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
if __name__ == "__main__":
    jira_authentication = authentication()