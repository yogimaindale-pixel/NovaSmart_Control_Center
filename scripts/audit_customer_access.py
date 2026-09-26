import subprocess
import json

cmd = """gcloud logging read 'resource.type="bigquery_resource" OR protoPayload.serviceName="bigquery.googleapis.com"' --limit=500 --format=json"""
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)

try:
    entries = json.loads(res.stdout)
    print(f"Total entries fetched: {len(entries)}")
    customer_access_events = []
    for e in entries:
        payload = e.get("protoPayload", {})
        principal = payload.get("authenticationInfo", {}).get("principalEmail", "Unknown")
        timestamp = e.get("timestamp")
        
        job = payload.get("serviceData", {}).get("jobCompletedEvent", {}).get("job", {})
        query = job.get("jobConfiguration", {}).get("query", {}).get("query", "")
        res_name = payload.get("resourceName", "")
        user_agent = payload.get("requestMetadata", {}).get("callerSuppliedUserAgent", "")
        
        if "customer_data" in query.lower() or "customer_data" in res_name.lower() or "customers" in query.lower():
            customer_access_events.append({
                "timestamp": timestamp,
                "principal": principal,
                "query": query if query else res_name,
                "user_agent": user_agent,
                "caller_ip": payload.get("requestMetadata", {}).get("callerIp", "")
            })
            
    print(f"\nFound {len(customer_access_events)} access log entries for customer_data:")
    for q in customer_access_events:
        print(f"[{q['timestamp']}] Principal: {q['principal']}")
        print(f"  Caller IP: {q['caller_ip']} | User-Agent: {q['user_agent']}")
        print(f"  Details/Query: {q['query']}")
        print("-" * 50)
except Exception as err:
    print("Error:", err)
