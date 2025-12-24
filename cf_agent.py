import requests
import os
import dotenv

dotenv.load_dotenv()

CF_API_KEY = os.getenv("CF_API_KEY")
CF_ZONE_ID = os.getenv("CF_ZONE_ID")
PUB_IP = os.getenv("PUB_IP")

if not CF_API_KEY or not CF_ZONE_ID:
    raise ValueError(
        "One or more required environment variables are missing: CF_API_KEY, CF_ZONE_ID"
    )

def create_dns_record(fulldomain):
    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CF_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": fulldomain,
        "content": PUB_IP,
        "proxied": True
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to create DNS record: {response.text}")
    else:
        print(f"Successfully created DNS record for {fulldomain}")
    return response.json()