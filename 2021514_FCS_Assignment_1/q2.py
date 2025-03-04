import base64
import hmac
import json
import itertools
import string 
from tqdm import tqdm

header_b64 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
payload_b64 = "eyJzdWIiOiJmY3MtYXNzaWdubWVudC0xIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2NzI1MTE0MDAsInJvbGUiOiJ1c2VyIiwiZW1haWwiOiJhcnVuQGlpaXRkLmFjLmluIiwiaGludCI6Imxvd2VyY2FzZS1hbHBoYW51bWVyaWMtbGVuZ3RoLTUifQ"
signature_given = "LCIyPHqWAVNLT8BMXw8_69TPkvabp57ZELxpzom8FiI"


def verifyjwt(token, secret):
    header, payload, signature = token.split('.')
    decoded_payload = json.loads(base64.urlsafe_b64decode(payload + '===').decode('utf-8'))
    decoded_header = json.loads(base64.urlsafe_b64decode(header + '===').decode('utf-8'))

    if decoded_header['alg'] not in ['HS256', 'HS384']:
        return "Invalid algorithm"
    if decoded_header['typ'] == "HS256":
        calculated_signature = hmac.new(secret.encode(), f"{header}.{payload}".encode(), 'sha256').digest()
    elif decoded_header['typ'] == "HS384":
        calculated_signature = hmac.new(secret.encode(), f"{header}.{payload}".encode(), 'sha384').digest()

    calculated_signature = base64.urlsafe_b64encode(calculated_signature).decode('utf-8').rstrip('=')
    if calculated_signature == signature:
        return decoded_payload
    else:
        return "Invalid signature"
header, payload, signature = header_b64, payload_b64, signature_given
decoded_payload = json.loads(base64.urlsafe_b64decode(payload + '===').decode('utf-8'))
decoded_header = json.loads(base64.urlsafe_b64decode(header + '===').decode('utf-8'))
print("Decoded payload and header:\n")
print(decoded_payload)
print(decoded_header)


import itertools
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmY3MtYXNzaWdubWVudC0xIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2NzI1MTE0MDAsInJvbGUiOiJ1c2VyIiwiZW1haWwiOiJhcnVuQGlpaXRkLmFjLmluIiwiaGludCI6Imxvd2VyY2FzZS1hbHBoYW51bWVyaWMtbGVuZ3RoLTUifQ.LCIyPHqWAVNLT8BMXw8_69TPkvabp57ZELxpzom8FiI"
header, payload, signature = token.split('.')

charset = "abcdefghijklmnopqrstuvwxyz0123456789"
print("\nSearching for secret key....\n")
for combo in tqdm(itertools.product(charset, repeat=5)):
    secret = ''.join(combo)
    decoded_payload = json.loads(base64.urlsafe_b64decode(payload + '===').decode('utf-8'))
    decoded_header = json.loads(base64.urlsafe_b64decode(header + '===').decode('utf-8'))
    calculated_signature = hmac.new(secret.encode(), f"{header}.{payload}".encode(), 'sha256').digest()
    calculated_signature = base64.urlsafe_b64encode(calculated_signature).decode('utf-8').rstrip('=')
    if calculated_signature == signature:
        print("\nFound Secret key: ",secret)
        break

    
print("\nNEW JWT TOKEN:")
new_payload = decoded_payload
new_payload['role'] = 'admin'
new_payload = base64.urlsafe_b64encode(json.dumps(new_payload).encode()).decode('utf-8').rstrip('=')
new_signature = hmac.new(secret.encode(), f"{header}.{new_payload}".encode(), 'sha256').digest()
new_signature = base64.urlsafe_b64encode(new_signature).decode('utf-8').rstrip('=')
new_token = f"{header}.{new_payload}.{new_signature}"
print(new_token)