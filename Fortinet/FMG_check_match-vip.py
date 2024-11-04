import requests
import argparse

# Base URL for FortiManager API
def get_base_url(ip):
    return f'https://{ip}/jsonrpc'

def login(base_url, username, password):
    """Authenticate and get session ID."""
    payload = {
        "method": "exec",
        "params": [
            {
                "url": "/sys/login/user",
                "data": {
                    "user": username,
                    "passwd": password
                }
            }
        ],
        "id": 1
    }
    response = requests.post(base_url, json=payload, verify=False)
    response_data = response.json()
    if response_data['result'][0]['status']['code'] == 0:
        session_id = response_data['session']
        print("Login successful")
        return session_id
    else:
        raise Exception("Login failed")

def get_policies(base_url, session_id, vdom):
    """Retrieve all policies from FortiManager."""
    payload = {
        "method": "get",
        "params": [
            {
                "url": f"/pm/config/adom/root/pkg/{vdom}/firewall/policy"
            }
        ],
        "session": session_id,
        "id": 1
    }
    response = requests.post(base_url, json=payload, verify=False)
    return response.json()

def update_policy(base_url, session_id, policy_id, vdom):
    """Update policy to enable match-vip if action is deny."""
    payload = {
        "method": "update",
        "params": [
            {
                "url": f"/pm/config/adom/root/pkg/{vdom}/firewall/policy/{policy_id}",
                "data": {
                    "match-vip": "enable"
                }
            }
        ],
        "session": session_id,
        "id": 1
    }
    response = requests.post(base_url, json=payload, verify=False)
    return response.json()

def logout(base_url, session_id):
    """Logout from FortiManager."""
    payload = {
        "method": "exec",
        "params": [
            {
                "url": "/sys/logout"
            }
        ],
        "session": session_id,
        "id": 1
    }
    requests.post(base_url, json=payload, verify=False)
    print("Logged out")

def main(fortimanager_ip, username, password, vdom):
    # Step 1: Construct base URL
    base_url = get_base_url(fortimanager_ip)

    try:
        # Step 2: Login and get session
        session_id = login(base_url, username, password)

        # Step 3: Get all policies
        policies = get_policies(base_url, session_id, vdom)
        
        # Step 4: Check each policy and update if action is deny
        for policy in policies['result'][0]['data']:
            policy_id = policy['policyid']
            action = policy['action']
            
            if action == 'deny':
                print(f"Policy {policy_id} has action 'deny'. Updating 'match-vip' to enable.")
                update_response = update_policy(base_url, session_id, policy_id, vdom)
                if update_response['result'][0]['status']['code'] == 0:
                    print(f"Policy {policy_id} updated successfully.")
                else:
                    print(f"Failed to update policy {policy_id}.")
            else:
                print(f"Policy {policy_id} does not have action 'deny', skipping.")

    finally:
        # Step 5: Logout
        logout(base_url, session_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FortiManager Policy Checker")
    parser.add_argument("-i", "--ip", required=True, help="IP address of the FortiManager")
    parser.add_argument("-u", "--username", required=True, help="Username for FortiManager")
    parser.add_argument("-p", "--password", required=True, help="Password for FortiManager")
    parser.add_argument("-v", "--vdom", required=True, help="VDOM for FortiManager")

    args = parser.parse_args()
    main(args.ip, args.username, args.password, args.vdom)
