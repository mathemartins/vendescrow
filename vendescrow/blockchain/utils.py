# Transfer other crypto assets
import json

from block_io import BlockIo

api_key: str = 'SArLt56DvARM0VAh'
api_secret: str = 'Esmed2FEtkAyAo44vomRFKipLfflbZh0'

# BLOCK IO 16 digit secret
pin: str = 'MA5aDzFyqXSFTXtB'
unique_phrase: str = 'unique nose deer nation athlete mask smart where cloud point grid east'

litecoin: str = '424f-f409-0198-4f79'
bitcoin: str = '413d-28c6-cc3c-10b3'
dogecoin: str = '2369-cce8-ec84-e3fa'
litecoin_testnet: str = 'f0c1-4225-3466-1f69'
bitcoin_testnet: str = '75c8-afcc-010a-83a5'
dogecoin_testnet: str = '2ff6-9bd9-ed93-a1b0'
version: int = 2

proxies = {
    "http": 'http://boyadxvkfgh1vg:8vp5w497ozwe7a81ocjb9koklxqmk2@us-east-static-06.quotaguard.com:9293',
    "https": 'http://boyadxvkfgh1vg:8vp5w497ozwe7a81ocjb9koklxqmk2@us-east-static-06.quotaguard.com:9293',
}


def create_address(username: str, crypto_network_api: str) -> str:
    import requests
    url = "https://block.io/api/v2/get_new_address/?api_key={apiKey}&label={username}".format(apiKey=crypto_network_api,
                                                                                              username=username)
    res = requests.get(url=url, proxies=proxies)
    return json.loads(res.content.decode('utf-8'))


def get_network_fee(crypto_network_api: str, receiver_address: str, amount: str):
        import requests

        network_fee_url = "https://block.io/api/v2/get_network_fee_estimate/?api_key={apiKey}&to_addresses={receiver_address}&amounts={amount}".format(
            apiKey=crypto_network_api,
            receiver_address=receiver_address,
            amount=amount,
        )
        network_fee_res = requests.get(url=network_fee_url, proxies=proxies)
        network_fee_data: dict = json.loads(network_fee_res.content.decode('utf-8'))
        return network_fee_data['data'].get('estimated_network_fee')


def transfer_crypto_with_sender_address(crypto_network_api: str, receiver_address: str, amount: str):
    print(crypto_network_api)
    import requests
    url = "https://block.io/api/v2/prepare_transaction/?api_key={apiKey}&to_addresses={receiver_address}&amounts={amount}".format(
        apiKey=crypto_network_api,
        receiver_address=receiver_address,
        amount=amount,
    )
    res = requests.get(url=url, proxies=proxies)
    prepare_trx: dict = json.loads(res.content.decode('utf-8'))
    print(prepare_trx)

    block_io = BlockIo(crypto_network_api, pin, version)
    block_io.summarize_prepared_transaction(prepare_trx)
    thisCheck = block_io.create_and_sign_transaction(prepare_data=prepare_trx)

    print(thisCheck, type(thisCheck))

    headers = {'Content-Type': 'application/json'}
    params = (('api_key', crypto_network_api),)
    data = {'transaction_data': thisCheck}

    trx_hash = requests.post('https://block.io/api/v2/submit_transaction/', headers=headers, params=params, data=json.dumps(data), proxies=proxies)
    print(trx_hash.text, trx_hash)
    return trx_hash.json()


# Vendescrow get Crypto Asset
def get_vendescrow_address_list(page_number: int, crypto_network_api: str):
    block_io = BlockIo(crypto_network_api, pin, version)
    return block_io.get_my_addresses(page=page_number)


# Get general balance
def get_balance(crypto_network_api: str):
    block_io = BlockIo(crypto_network_api, pin, version)
    return block_io.get_balance()


# Get wallet balance
def get_wallet_balance(crypto_network_api: str, address):
    block_io = BlockIo(crypto_network_api, pin, version)
    return block_io.get_address_balance(addresses=address)


# Get archive address
def get_archive_address(crypto_network_api: str, label):
    block_io = BlockIo(crypto_network_api, pin, version)
    return block_io.archive_addresses(label=label)
