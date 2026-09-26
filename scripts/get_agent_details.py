import os
import json
import requests
import google.auth
from google.auth.transport.requests import Request

project = "qwiklabs-gcp-01-2aad14f2c696"
credentials, project_id = google.auth.default()
credentials.refresh(Request())
token = credentials.token
headers = {"Authorization": f"Bearer {token}"}

regions = ["us-west1", "us-central1", "us-east1", "europe-west1", "europe-west2", "asia-east1", "global", "us"]

all_details = {}

for loc in regions:
    url = f"https://agentregistry.googleapis.com/v1/projects/{project}/locations/{loc}/agents"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        agents = data.get("agents", [])
        for a in agents:
            agent_id = a.get("name")
            # Get detail of this agent
            detail_resp = requests.get(f"https://agentregistry.googleapis.com/v1/{agent_id}", headers=headers)
            if detail_resp.status_code == 200:
                all_details[agent_id] = detail_resp.json()
            else:
                all_details[agent_id] = a

print(json.dumps(all_details, indent=2))
