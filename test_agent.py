import requests
import json

URL = "http://127.0.0.1:8000/agent"
BASE_URL = "http://127.0.0.1:8000"

payload = {
    "request": "Draft a comprehensive onboarding standard operating procedure (SOP) for a remote engineering team."
}

print("🚀 Sending request to Autonomous Agent...")
response = requests.post(URL, json=payload)

if response.status_code == 200:
    data = response.json()
    print("\n✅ Agent Execution Complete!")
    print(f"Rationale: {data['rationale']}")
    print(f"Assumptions Made: {data['assumptions_made']}")
    print("\nExecution Logs:")
    for log in data['execution_log']:
        print(f" - {log}")
        
    # Download the final artifact
    download_link = BASE_URL + data['download_url']
    print(f"\n📥 Downloading file from: {download_link}")
    doc_response = requests.get(download_link)
    
    filename = data['download_url'].split('/')[-1]
    with open(filename, "wb") as f:
        f.write(doc_response.content)
    print(f"💾 File successfully saved locally as: {filename}")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")