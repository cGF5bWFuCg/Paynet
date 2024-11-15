import csv
import requests
import argparse
import json

# Function to add object to FortiManager
def add_object_to_fortimanager(fmg_ip, api_token, adom, data, success_list, failure_list):
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
            success_list.append(data['name'])
        else:
            print(f"Failed to add object: {data['name']}, Response: {response.json()}")
            failure_list.append((data['name'], response.json()))
    else:
        print(f"Failed to add object: {data['name']}, Status Code: {response.status_code}, Response: {response.text}")
        failure_list.append((data['name'], response.text))

# Function to create address object
def create_address_object(row, fmg_ip, api_token, adom, success_list, failure_list):
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
            failure_list.append((row['name'], "Missing subnet"))
            return
    elif obj_type == 'iprange':
        if row['start_ip'] and row['end_ip']:
            data["start-ip"] = row['start_ip']
            data["end-ip"] = row['end_ip']
        else:
            print(f"Error: Missing IP range for {row['name']}")
            failure_list.append((row['name'], "Missing IP range"))
            return
    elif obj_type == 'fqdn':
        if row['fqdn']:
            data["fqdn"] = row['fqdn']
        else:
            print(f"Error: No FQDN provided for {row['name']}")
            failure_list.append((row['name'], "Missing FQDN"))
            return
    elif obj_type == 'geography':
        if row['country']:
            data["country"] = row['country']
        else:
            print(f"Error: No country provided for {row['name']}")
            failure_list.append((row['name'], "Missing country"))
            return
    elif obj_type == 'wildcard':
        if row['subnet']:
            data["subnet"] = row['subnet']
        else:
            print(f"Error: No subnet provided for {row['name']}")
            failure_list.append((row['name'], "Missing subnet"))
            return
    elif obj_type == 'wildcard-fqdn':
        if row['fqdn']:
            data["fqdn"] = row['fqdn']
        else:
            print(f"Error: No FQDN provided for {row['name']}")
            failure_list.append((row['name'], "Missing FQDN"))
            return

    # Send the data to FortiManager
    add_object_to_fortimanager(fmg_ip, api_token, adom, data, success_list, failure_list)

# Main function to handle CSV and arguments
def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="FortiManager Address Importer")
    parser.add_argument("-i", "--ip", required=True, help="FortiManager IP address")
    parser.add_argument("-t", "--token", required=True, help="FortiManager API token")
    parser.add_argument("-a", "--adom", required=True, help="Administrative Domain (ADOM) in FortiManager")
    parser.add_argument("-f", "--file", required=True, help="Path to the CSV file")
    
    args = parser.parse_args()

    # Lists to track success and failure of each object addition
    success_list = []
    failure_list = []

    # Reading CSV file with specified delimiter and encoding
    with open(args.file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # specify delimiter as ';'
        print("Headers:", reader.fieldnames)  # Debugging line to print headers
        for row in reader:
            create_address_object(row, args.ip, args.token, args.adom, success_list, failure_list)

    # Final summary of success and failure
    print("\n> Summary Report:")
    print("> ---------------")
    print(f"> Total Successful Additions: {len(success_list)}")
    for name in success_list:
        print(f">> {name}")
    print(f"> Total Failed Additions: {len(failure_list)}")
    for name, reason in failure_list:
        print(f">> {name}: \n>>> {reason}\n")

if __name__ == "__main__":
    main()

