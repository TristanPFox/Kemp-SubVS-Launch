import requests
import json
import dotenv
import os
import urllib3
import warnings

# Disable SSL warnings
urllib3.disable_warnings()
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

dotenv.load_dotenv()

API_KEY = os.getenv("KEMP_API_KEY")
VS_IP = os.getenv("KEMP_VS_IP")
KEMP_URL = os.getenv("KEMP_URL")

if not API_KEY or not VS_IP or not KEMP_URL:
    raise ValueError(
        "One or more required environment variables are missing: KEMP_API_KEY, KEMP_VS_IP, KEMP_URL"
    )

URL = f"{KEMP_URL}/accessv2"


# Show list of virtual services - DEBUGGING
def vs_list():
    body = {"cmd": "listvs", "apikey": API_KEY}
    response = requests.post(URL, json=body, verify=False)

    # Print json response cleanly
    json_response = response.json()
    print(json.dumps(json_response, indent=4))


# Create a new SubVS
def add_subvs():
    body = {
        "cmd": "modvs",
        "apikey": API_KEY,
        "vs": VS_IP,
        "port": "443",
        "prot": "tcp",
        "createsubvs": "",
    }
    response = requests.post(URL, json=body, verify=False)

    # Print json response cleanly
    json_response = response.json()

    if response.status_code != 200:
        raise ValueError(f"Failed to add SubVS: {json_response}")
    else:
        print(
            f"SubVS added successfully with ID: {json_response['SubVS'][-1]['VSIndex']}"
        )

    return json_response["SubVS"][-1]["VSIndex"]
    # print(json.dumps(json_response, indent=4))


# Modify an existing SubVS to add a nickname and update HTTP check method
def mod_subvs(vs_index, name):
    body = {
        "cmd": "modvs",
        "apikey": API_KEY,
        "vs": str(vs_index),
        "nickname": name,
        "checkuseget": 1,  # HTTP Method GET
    }
    response = requests.post(URL, json=body, verify=False)

    # Print json response cleanly
    json_response = response.json()
    # print(json.dumps(json_response, indent=4))
    if response.status_code != 200:
        raise ValueError(f"Failed to modify SubVS: {json_response}")
    else:
        print(f"SubVS Name and HTTP check method updated successfully.")


# Show content rules - DEBUGGING
def show_rules():
    body = {"cmd": "showrule", "apikey": API_KEY}
    response = requests.post(URL, json=body, verify=False)

    # Print json response cleanly
    json_response = response.json()
    print(json.dumps(json_response, indent=4))


# Add a new content rule
def add_rule(domain, name):
    body = {
        "cmd": "addrule",
        "apikey": API_KEY,
        "name": name,
        "type": "0",
        "pattern": f"^{domain}",
        "header": "host",
        "nocase": True,
    }
    response = requests.post(URL, json=body, verify=False)

    # Print json response cleanly
    json_response = response.json()
    # print(json.dumps(json_response, indent=4))
    if response.status_code != 200:
        raise ValueError(f"Failed to add rule: {json_response}")
    else:
        print(f"Rule added successfully.")


# Add a new real server to a SubVS
def add_real_server(vs_id, real_server, real_port):
    body = {
        "cmd": "addrs",
        "apikey": API_KEY,
        "vs": vs_id,
        "port": real_port,
        "prot": "tcp",
        "rs": real_server,
        "rsport": real_port,
    }
    response = requests.post(URL, json=body, verify=False)

    # Print json response cleanly
    json_response = response.json()
    # print(json.dumps(json_response, indent=4))
    if response.status_code != 200:
        raise ValueError(f"Failed to add real server: {json_response}")
    else:
        print(f"Real server added successfully.")

    return json_response
