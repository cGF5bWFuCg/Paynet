import csv
import requests
import argparse
import json

# Function to add object to FortiManager
def add_object_to_fortimanager(fmg_ip, api_token, adom, data):
    api_url = f"https://{fmg_ip}/jsonrpc"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # JSON-RPC payload structure for FortiManager
    payload = {
        "method": "add",
        "params": [{
            "url": f"/pm/config/adom/{adom}/obj/firewall/address",
            "data": data
        }],
        "session": api_token,
        "id": 1
    }

    # Print data for debugging
    print(f"Sending data to FortiManager: {data}")
    
    response = requests.post(api_url, headers=headers, json=payload, verify=False)
    
    if response.status_code == 200:
        result = response.json().get("result", [])
        if result and result[0].get("status", {}).get("code") == 0:
            print(f"Successfully added object: {data['name']}")
        else:
            print(f"Failed to add object: {data['name']}, Response: {response.json()}")
    else:
        print(f"Failed to add object: {data['name']}, Status Code: {response.status_code}, Response: {response.text}")

# Function to create address object
def create_address_object(row, fmg_ip, api_token, adom):
    obj_type = row['type']
    data = {
        "name": row['name'],
        "comment": row['comment'],
        "type": obj_type,   # Explicitly set the type for FortiManager
        "color": "0"        # Optional field
    }
    # Set specific fields based on type
    if obj_type == 'ipmask':
        if row['subnet']:
            data["subnet"] = row['subnet']
        else:
            print(f"Error: No subnet provided for {row['name']}")
            return
    elif obj_type == 'iprange':
        if row['start_ip'] and row['end_ip']:
            data["start-ip"] = row['start_ip']
            data["end-ip"] = row['end_ip']
        else:
            print(f"Error: Missing IP range for {row['name']}")
            return
    elif obj_type == 'fqdn':
        if row['fqdn']:
            data["fqdn"] = row['fqdn']
        else:
            print(f"Error: No FQDN provided for {row['name']}")
            return
    elif obj_type == 'geography':
        if row['country']:
            data["country"] = row['country']
        else:
            print(f"Error: No country provided for {row['name']}")
            return
    elif obj_type == 'wildcard':
        if row['subnet']:
            data["subnet"] = row['subnet']
        else:
            print(f"Error: No subnet provided for {row['name']}")
            return
    # elif obj_type == 'mac':
    #     if row['macaddr']:
    #         data["macaddr"] = [{"macaddr": row['macaddr']}]
    #     else:
    #         print(f"Error: No MAC address provided for {row['name']}")
    #         return
    elif obj_type == 'wildcard-fqdn':
        if row['fqdn']:
            data["fqdn"] = row['fqdn']
        else:
            print(f"Error: No FQDN provided for {row['name']}")
            return

    # Send the data to FortiManager
    add_object_to_fortimanager(fmg_ip, api_token, adom, data)

# Main function to handle CSV and arguments
def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="FortiManager Address Importer")
    parser.add_argument("--ip", required=True, help="FortiManager IP address")
    parser.add_argument("--token", required=True, help="FortiManager API token")
    parser.add_argument("--adom", required=True, help="Administrative Domain (ADOM) in FortiManager")
    parser.add_argument("--file", required=True, help="Path to the CSV file")

    args = parser.parse_args()

    # Reading CSV file
    with open(args.file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            create_address_object(row, args.ip, args.token, args.adom)

if __name__ == "__main__":
    main()

# python import_object_to_fmg.py -i 192.168.1.1 -t your_api_token -a root -f objects.csv
# python import_object_to_fmg.py --ip 192.168.1.1 --token your_api_token --adom root --file objects.csv