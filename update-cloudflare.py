import requests
import os
import sys
import json
import subprocess
import time

REQUIRED_ENV_VARS = ["CLOUDFLARE_API_KEY", "CLOUDFLARE_ZONE_ID", "CLOUDFLARE_DOMAIN", "CLOUDFLARE_SUBDOMAINS"]
OPTIONAL_ENV_VARS = ["PROXY"]

def verify_necessary_config():
    missing_variables = []
    for variable in REQUIRED_ENV_VARS:
        if variable not in os.environ or not os.environ.get(variable):
            missing_variables.append(variable)
    
    if missing_variables:
        print(f"Some of required environment variables are missing. Missing variables={missing_variables}")
        sys.exit(1)

def get_current_public_ip():
    command = "dig +short myip.opendns.com @resolver1.opendns.com".split()
    akamai_command = "dig whoami.akamai.net. @ns1-1.akamaitech.net. +short".split()
    try:
        ip = subprocess.check_output(command)
    except Exception as e:
        print("Failed with opendns. Trying akamai")
        try:
            ip = subprocess.check_output(akamai_command)
        except Exception as e2:
            print("Failed to get current publicn IP Address")
            print(e)
            print(e2)
            sys.exit(1)

    ip = ip.strip().decode()
    return ip

def get_cloudflare_dns():
    url = f"https://api.cloudflare.com/client/v4/zones/{os.environ['CLOUDFLARE_ZONE_ID']}/dns_records"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['CLOUDFLARE_API_KEY']}"
    }
    out = requests.get(url, headers=headers)
    if out.status_code <200 or out.status_code >= 400:
        print(out)
        print(out.text)
        sys.exit(1)
    output = json.loads(out.text)
    results = output["result"]
    subdomains = os.environ['CLOUDFLARE_SUBDOMAINS'].split()
    for subdomain in subdomains:
        cloudflare_domain = f"{subdomain.strip()}.{os.environ['CLOUDFLARE_DOMAIN']}"
        returned = False
        for item in results:
            if item["zone_name"] == os.environ["CLOUDFLARE_DOMAIN"] and item["name"] == cloudflare_domain:
                returned = True
                yield item["content"], item["id"], ""
                break
        if not returned:
            yield None, None, f"No Cloudflare record found for {cloudflare_domain}"


def update_cloudflare_dns(public_ip, dns_id):
    url = f"https://api.cloudflare.com/client/v4/zones/{os.environ['CLOUDFLARE_ZONE_ID']}/dns_records/{dns_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['CLOUDFLARE_API_KEY']}"
    }
    request_data = {
        "content": public_ip,
    }
    if os.environ.get("CLOUDFLARE_PROXIED", None):
        request_data["proxied"] = bool(os.environ["CLOUDFLARE_PROXIED"])
    out = requests.patch(url, data=json.dumps(request_data), headers=headers)
    if out.status_code < 200 or out.status_code >=400:
        print("ERROR")
        print(json.loads(out.text))
        return 1
    return 0

def main():
    # Verify necessary variables are set
    verify_necessary_config()

    # Get current public IP address
    current_public_ip = get_current_public_ip()

    return_code = 0

    # Get current Cloudflare IP for subdomain
    for current_cloudflare_ip, dns_id, err in get_cloudflare_dns():
        if err:
            print(err)
            continue

        if current_public_ip == current_cloudflare_ip:
            print(f"IP has not changed since last run. public_ip={current_public_ip}, cloudflare_ip={current_cloudflare_ip}")
            return None

        return_code = update_cloudflare_dns(current_public_ip, dns_id)

    return return_code

if __name__ == "__main__":
    while True:
        try:
            main()
            time.sleep(300)
        except SystemExit:
            print("FAILED. EXITING")
            break
        except:
            print("FAILED... RETRYING")
            time.sleep(300)
