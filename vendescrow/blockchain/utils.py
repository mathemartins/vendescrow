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
    "http": 'http://lq0qv9rvlok3pn:l8scv7gafgaiy0j3wxydmq0od1nuq@us-east-static-06.quotaguard.com:9293',
    "https": 'http://lq0qv9rvlok3pn:l8scv7gafgaiy0j3wxydmq0od1nuq@us-east-static-06.quotaguard.com:9293',
}


def create_address(username: str, crypto_network_api: str) -> str:
    import requests
    url = "https://block.io/api/v2/get_new_address/?api_key={apiKey}&label={username}".format(apiKey=crypto_network_api,
                                                                                              username=username)
    res = requests.get(url=url, proxies=proxies)
    return json.loads(res.content.decode('utf-8'))


"""
2 DOGE, 0.00002 BTC, 0.0002LTC
"""


# Transfer Crypto Asset For Vendescrow
def transfer_crypto_for_vend(amount: str, sender_address: str, receiver_address: str, crypto_network_api: str,
                             priority: str):
    if 'litecoin' in crypto_network_api and float(amount) <= 0.0002:
        return json.dumps(
            {'status': 'error', 'data': {'message': 'Cannot transfer {value} or less'.format(value=float(amount))}})
    if 'bitcoin' in crypto_network_api and float(amount) <= 0.00002:
        return json.dumps(
            {'status': 'error', 'data': {'message': 'Cannot transfer {value} or less'.format(value=float(amount))}})
    if 'dogecoin' in crypto_network_api and float(amount) <= 2:
        return json.dumps(
            {'status': 'error', 'data': {'message': 'Cannot transfer {value} or less'.format(value=float(amount))}})
    block_io = BlockIo(crypto_network_api, pin, version)
    prepare_trx = block_io.prepare_transaction(amounts=amount, from_addresses=sender_address,
                                               to_addresses=receiver_address, priority=priority)
    block_io.summarize_prepared_transaction(prepare_trx)
    create_and_sign_trx = block_io.create_and_sign_transaction(prepare_trx)
    return block_io.submit_transaction(transaction_data=create_and_sign_trx)


def transfer_crypto_with_sender_address(crypto_network_api: str, sender_address: str, receiver_address: str,
                                        amount: str):
    import requests
    url = "https://block.io/api/v2/prepare_transaction/?api_key={apiKey}&from_addresses={sender_address}&to_addresses={receiver_address}&amounts={amount}".format(
        apiKey=crypto_network_api,
        sender_address=sender_address,
        receiver_address=receiver_address,
        amount=amount,
    )
    res = requests.get(url=url, proxies=proxies)
    prepare_trx = json.loads(res.content.decode('utf-8'))

    input = prepare_trx['data'].get('inputs')
    output = prepare_trx['data'].get('outputs')
    encrypted_user_key = prepare_trx['data']['user_key'].get('encrypted_passphrase')
    input_address_data = prepare_trx['data'].get('input_address_data')

    block_io = BlockIo(crypto_network_api, pin, version)
    block_io.summarize_prepared_transaction(prepare_trx)
    thisCheck = block_io.create_and_sign_transaction(prepare_data=prepare_trx)
    print(thisCheck)
    trx_hash = block_io.submit_transaction(transaction_data=thisCheck)
    print(trx_hash)
    return trx_hash


# Transfer Crypto Asset
def transfer_crypto(amount: str, receiver_address: str, crypto_network_api: str, priority: str):
    if 'litecoin' in crypto_network_api and float(amount) <= 0.0002:
        return json.dumps(
            {'status': 'error', 'data': {'message': 'Cannot transfer {value} or less'.format(value=float(amount))}})
    if 'bitcoin' in crypto_network_api and float(amount) <= 0.00002:
        return json.dumps(
            {'status': 'error', 'data': {'message': 'Cannot transfer {value} or less'.format(value=float(amount))}})
    if 'dogecoin' in crypto_network_api and float(amount) <= 2:
        return json.dumps(
            {'status': 'error', 'data': {'message': 'Cannot transfer {value} or less'.format(value=float(amount))}})
    block_io = BlockIo(crypto_network_api, pin, version)
    prepare_trx = block_io.prepare_transaction(amounts=amount, to_addresses=receiver_address, priority=priority)
    block_io.summarize_prepared_transaction(prepare_trx)
    create_and_sign_trx = block_io.create_and_sign_transaction(prepare_trx)
    return block_io.submit_transaction(transaction_data=create_and_sign_trx)


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
