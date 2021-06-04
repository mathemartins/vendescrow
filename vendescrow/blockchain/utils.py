# Transfer other crypto assets

from blockcypher import from_base_unit

api_key: str = '79d9c1fb002c4543a0befb9e83d81a5c'


# Convert BTC to satoshi and vice versa
def asset_conversion(amount, type):
    if type == 'btc':
        return amount * 100000000
    return from_base_unit(amount, 'btc')


# def transfer():
#     pass
#
# crypto_api_io: str = '92f919592e3d6d6d18d1e0cf5b1e99e3ea035b22'
# import requests
# url = 'https://api.cryptoapis.io/v1/bc/btc/testnet/info'
# headers = {
#   "Content-Type": "application/json",
#   "X-API-Key": crypto_api_io
# }
# response = requests.get(url, headers=headers)










"""
import requests

conn = "https://rest.cryptoapis.io/v2/blockchain-data/bitcoin/testnet/blocks/last"
headers = {
  'Content-Type': "application/json",
  'X-API-Key': crypto_api_io
}
response = requests.get(conn, headers=headers)

import http.client

conn = http.client.HTTPConnection("https://rest.cryptoapis.io/v2")
headers = {
  'Content-Type': "application/json",
  'X-API-Key': "my-api-key"
}

conn.request("GET", "blockchain-data/bitcoin/testnet/blocks/last", headers=headers )

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))



import requests
crypto_api_io: str = '92f919592e3d6d6d18d1e0cf5b1e99e3ea035b22'
url = "https://api.cryptoapis.io/v1/bc/btc/testnet/txs/create"

payload = "{\n    \"inputs\": [{\n        \"address\": \"tb1qw4383dp9v8gmf25sqar7n8fmees7df6k8nuskc\",\n        \"value\": 0.0008\n    }],\n    \"outputs\": [{\n        \"address\": \"tb1qg5wunxsn9sca9jz3etgnxe3h33km2wnsjjyd73\",\n        \"value\": 0.0008\n    }],\n    \"fee\":  {\n    \t\"address\" : \"tb1qw4383dp9v8gmf25sqar7n8fmees7df6k8nuskc\",\n        \"value\": 0.00023141\n    },\n    \"data\": \"CRYPTOAPISROCKS\",\n    \"replaceable\": true\n}"
 
headers = {
  "Content-Type": "application/json",
  "X-API-Key": crypto_api_io
}
response = requests.request("POST", url, json=payload, headers=headers)
"""