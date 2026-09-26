import subprocess
import json

def run(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

print("=== IAM Policy for Project ===")
iam_json = run("gcloud projects get-iam-policy qwiklabs-gcp-01-2aad14f2c696 --format=json")
try:
    policy = json.loads(iam_json)
    for b in policy.get("bindings", []):
        role = b.get("role")
        if "bigquery" in role.lower() or "owner" in role.lower() or "editor" in role.lower() or "admin" in role.lower():
            print(f"Role: {role}")
            for m in b.get("members", []):
                print(f"  - {m}")
except Exception as e:
    print("Error parsing IAM policy:", e)

print("\n=== Cloud Run Service Accounts ===")
services = [
    ("novasmart-mcp", "us-west1"),
    ("novasmart-store-portal", "us-west1"),
    ("promo-agent-shadow", "us-west1"),
    ("remote-browser-vm1", "europe-west2"),
    ("smart-recipe-assistant-frontend", "us-central1")
]
for svc, region in services:
    sa = run(f"gcloud run services describe {svc} --region={region} --format='value(spec.template.spec.serviceAccountName)'")
    print(f"Service {svc} ({region}): {sa if sa else 'Default Compute SA'}")

print("\n=== Dataset customer_data Access Control List ===")
ds_json = run("bq show --format=prettyjson customer_data")
try:
    ds = json.loads(ds_json)
    access = ds.get("access", [])
    for a in access:
        print(json.dumps(a))
except Exception as e:
    print("Error parsing dataset ACL:", e)
