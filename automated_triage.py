from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from create_ticket import create_jira_ticket
from mangum import Mangum  # only needed for Lambda compatibility

app = FastAPI()

# Define JSON input model
class TicketRequest(BaseModel):
    project_key: str
    summary: str
    description: str
    issue_type: str = "Bug"  # Optional, defaults to "Bug" if not given

# Define API route
@app.post("/create-ticket")
def create_ticket(request: TicketRequest):
    """
    Endpoint to create a Jira ticket.
    """
    result = create_jira_ticket(
        project_key=request.project_key,
        summary=request.summary,
        description=request.description,
        issue_type=request.issue_type
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Ticket creation failed"))

    return result

# For AWS Lambda Deployment
handler = Mangum(app)

aws lambda invoke --function-name automated-triage-function  --payload '{
    "project_key": "INFRAOPS",
    "summary": "Test Issue",
    "description": "Description of the test issue",
    "issue_type": "Bug"
  }'
