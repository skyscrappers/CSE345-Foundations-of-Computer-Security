#get all the subdomains of a domain using crt.sh
import requests
import sys
import re
import json

def get_subdomains(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        sys.exit(1)
    data = response.json()
    subdomains = set()
    for entry in data:
        name = entry["name_value"]
        subdomains.add(name)
    return subdomains

subdomains_crt = get_subdomains("iiitd.edu.in")
print("Fetched all subdomains from crt.sh......\n")

# Function to fetch subdomains from DNSDumpster API
def get_subdomains_dnsdumpster(domain, api_key):
    url = f"https://api.dnsdumpster.com/domain/{domain}" 
    headers = {
        'X-API-KEY': api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        sys.exit(1)
    data = response.json()
    subdomains = set()
    for i in data['a']:
        subdomains.add(i['host'])
    return subdomains


subdomains_dns = get_subdomains_dnsdumpster("iiitd.edu.in", "b500065055066a34fa909bbc2dbb440c22612c619ecfcec41859d51a41e61169")
print("Fetched all subdomains from DNSDumpster API......\n")
all_subdomains = subdomains_crt.union(subdomains_dns)
print("Total subdomains: ",len(all_subdomains))
import socket
# fetch the private IP addresses of these subdomains and list them (subdomain:[PRIVATE_IP]).
def get_private_ip(subdomains):
    private_ip = {}
    for subdomain in subdomains:
        try:
            ip = socket.gethostbyname(subdomain)
            if re.match(r'^(10|172|192)\.', ip):
                private_ip[subdomain] = ip
        except:
            pass
    return private_ip

private_ip = get_private_ip(all_subdomains)

print("Private IP addresses of subdomains:\n")
for subdomain, ip in private_ip.items():
    print(f"{subdomain}: {ip}")