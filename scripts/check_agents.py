import os
import requests
from google.cloud import aiplatform

project = "qwiklabs-gcp-01-2aad14f2c696"
regions = ["us-west1", "us-central1", "us-east1", "europe-west1", "europe-west2", "asia-east1"]

print("=== Checking Vertex AI Reasoning Engines (Agent Runtime) ===")
for region in regions:
    aiplatform.init(project=project, location=region)
    try:
        engines = aiplatform.ReasoningEngine.list()
        print(f"Region: {region} -> Found {len(engines)} Reasoning Engines:")
        for eng in engines:
            print(f"  - Display Name: {eng.display_name}")
            print(f"    Resource Name: {eng.resource_name}")
            print(f"    Description: {eng.description}")
    except Exception as e:
        print(f"Region: {region} -> Error: {e}")

print("\n=== Checking Agent Registry (via gcloud / REST API) ===")
import google.auth
from google.auth.transport.requests import Request

credentials, project_id = google.auth.default()
credentials.refresh(Request())
token = credentials.token
headers = {"Authorization": f"Bearer {token}"}

for loc in regions + ["global", "us", "eu"]:
    url = f"https://agentregistry.googleapis.com/v1/projects/{project}/locations/{loc}/agents"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        agents = data.get("agents", [])
        print(f"Location {loc}: {len(agents)} agents found")
        for a in agents:
            print(f"  - {a.get('name')}: {a.get('displayName')}")
    else:
        # Check services endpoint
        url_svc = f"https://agentregistry.googleapis.com/v1/projects/{project}/locations/{loc}/services"
        resp_svc = requests.get(url_svc, headers=headers)
        if resp_svc.status_code == 200:
            data_svc = resp_svc.json()
            services = data_svc.get("services", [])
            print(f"Location {loc} (Services): {len(services)} services found")
            for s in services:
                print(f"  - {s.get('name')}: {s.get('displayName')}")
