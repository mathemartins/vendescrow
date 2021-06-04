import json

from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from web3 import Web3

from vendescrow.blockchain.ethereum_constants import MAINNET_URL, GINACHE_URL
from vendescrow.blockchain.utils import asset_conversion
from wallets.models import EthereumWallet, TetherUSDWallet, BitcoinWallet, DogecoinWallet, LitecoinWallet, DashWallet

web3 = Web3(Web3.HTTPProvider(MAINNET_URL))


class BitcoinAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            import requests
            user_bitcoin_wallet = BitcoinWallet.objects.get(user=request.user)
            balance = requests.get(
                'https://api.blockcypher.com/v1/btc/test3/addrs/{address}/balance?token=79d9c1fb002c4543a0befb9e83d81a5c'.format(
                    address=user_bitcoin_wallet.address))
            jsonBal = balance.content.decode('utf-8').replace("'", '"')
            print(jsonBal)
            jsonBal = json.loads(jsonBal)
            print(type(jsonBal))
            balance_in_btc = float(jsonBal.get('balance')) / 100000000

            if balance_in_btc != float(user_bitcoin_wallet.previous_bal):
                added_asset = float(balance_in_btc) - float(user_bitcoin_wallet.previous_bal)
                print(added_asset)
                user_bitcoin_wallet.available = float(user_bitcoin_wallet.available) + added_asset
                user_bitcoin_wallet.previous_bal = float(user_bitcoin_wallet.previous_bal) + added_asset
                user_bitcoin_wallet.save()

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Bitcoin Address Retrieved',
                'data': [{
                    'username': request.user.username,
                    'name': user_bitcoin_wallet.name,
                    'balance': user_bitcoin_wallet.available,
                    'short_name': user_bitcoin_wallet.short_name,
                    'icon': user_bitcoin_wallet.icon,
                    'private': user_bitcoin_wallet.private_key,
                    'public': user_bitcoin_wallet.public_key,
                    'address': str(user_bitcoin_wallet.address),
                    'frozen': user_bitcoin_wallet.frozen,
                    'amount': user_bitcoin_wallet.amount,
                }]
            }
        except BitcoinWallet.DoesNotExist:
            import requests
            btc_account_request = requests.post(
                'https://api.blockcypher.com/v1/btc/test3/addrs?token=79d9c1fb002c4543a0befb9e83d81a5c&bech32=true')
            btc_account = btc_account_request.content.decode('utf-8').replace("'", '"')
            print(btc_account)
            btc_account = json.loads(btc_account)
            print(type(btc_account))
            btc_icon_url = 'https://cryptologos.cc/logos/bitcoin-btc-logo.png'

            new_btc_wallet = BitcoinWallet.objects.create(
                user=request.user,
                name='Bitcoin',
                short_name='BTC',
                icon=btc_icon_url,
                private_key=btc_account.get('private'),
                public_key=btc_account.get('public'),
                address=btc_account.get('address'),
                wif=btc_account.get('wif'),
            )

            balance = requests.get(
                'https://api.blockcypher.com/v1/btc/test3/addrs/{address}/balance?token=79d9c1fb002c4543a0befb9e83d81a5c'.format(
                    address=btc_account['address']))
            jsonBal = balance.content.decode('utf-8').replace("'", '"')
            jsonBal = json.loads(jsonBal)
            balance_in_btc = float(jsonBal.get('balance')) / 100000000

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Bitcoin Address Created',
                'data': [{
                    'username': request.user.username,
                    'name': new_btc_wallet.name,
                    'balance': balance_in_btc,
                    'short_name': new_btc_wallet.short_name,
                    'icon': btc_icon_url,
                    'private': new_btc_wallet.private_key,
                    'public': new_btc_wallet.public_key,
                    'address': str(new_btc_wallet.address),
                    'frozen': new_btc_wallet.frozen,
                    'amount': new_btc_wallet.amount,
                }]
            }
        return Response(response, status=status.HTTP_200_OK)


class DogecoinAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            import requests
            user_dogecoin_wallet = DogecoinWallet.objects.get(user=request.user)
            balance = requests.get(
                'https://api.blockcypher.com/v1/doge/main/addrs/{address}/balance?token=79d9c1fb002c4543a0befb9e83d81a5c'.format(
                    address=user_dogecoin_wallet.address))
            jsonBal = balance.content.decode('utf-8').replace("'", '"')
            print(jsonBal)
            jsonBal = json.loads(jsonBal)
            print(type(jsonBal))
            balance_in_doge = float(jsonBal.get('balance')) / 100000000

            if balance_in_doge != float(user_dogecoin_wallet.previous_bal):
                added_asset = float(balance_in_doge) - float(user_dogecoin_wallet.previous_bal)
                print(added_asset)
                user_dogecoin_wallet.available = float(user_dogecoin_wallet.available) + added_asset
                user_dogecoin_wallet.previous_bal = float(user_dogecoin_wallet.previous_bal) + added_asset
                user_dogecoin_wallet.save()

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Bitcoin Address Retrieved',
                'data': [{
                    'username': request.user.username,
                    'name': user_dogecoin_wallet.name,
                    'balance': user_dogecoin_wallet.available,
                    'short_name': user_dogecoin_wallet.short_name,
                    'icon': user_dogecoin_wallet.icon,
                    'private': user_dogecoin_wallet.private_key,
                    'public': user_dogecoin_wallet.public_key,
                    'address': str(user_dogecoin_wallet.address),
                    'frozen': user_dogecoin_wallet.frozen,
                    'amount': user_dogecoin_wallet.amount,
                }]
            }
        except DogecoinWallet.DoesNotExist:
            import requests
            doge_account_request = requests.post(
                'https://api.blockcypher.com/v1/doge/main/addrs?token=79d9c1fb002c4543a0befb9e83d81a5c&bech32=true')
            doge_account = doge_account_request.content.decode('utf-8').replace("'", '"')
            print(doge_account)
            doge_account = json.loads(doge_account)
            print(type(doge_account))
            doge_icon_url = 'https://cryptologos.cc/logos/bitcoin-btc-logo.png'

            new_doge_wallet = DogecoinWallet.objects.create(
                user=request.user,
                name='Dogecoin',
                short_name='DOGE',
                icon=doge_icon_url,
                private_key=doge_account.get('private'),
                public_key=doge_account.get('public'),
                address=doge_account.get('address'),
                wif=doge_account.get('wif'),
            )

            balance = requests.get(
                'https://api.blockcypher.com/v1/doge/main/addrs/{address}/balance?token=79d9c1fb002c4543a0befb9e83d81a5c'.format(
                    address=doge_account['address']))
            jsonBal = balance.content.decode('utf-8').replace("'", '"')
            jsonBal = json.loads(jsonBal)
            balance_in_doge = float(jsonBal.get('balance')) / 100000000

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Dogecoin Address Created',
                'data': [{
                    'username': request.user.username,
                    'name': new_doge_wallet.name,
                    'balance': balance_in_doge,
                    'short_name': new_doge_wallet.short_name,
                    'icon': doge_icon_url,
                    'private': new_doge_wallet.private_key,
                    'public': new_doge_wallet.public_key,
                    'address': str(new_doge_wallet.address),
                    'frozen': new_doge_wallet.frozen,
                    'amount': new_doge_wallet.amount,
                }]
            }
        return Response(response, status=status.HTTP_200_OK)


class LitecoinAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            import requests
            user_litecoin_wallet = LitecoinWallet.objects.get(user=request.user)
            balance = requests.get(
                'https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance?token=79d9c1fb002c4543a0befb9e83d81a5c'.format(
                    address=user_litecoin_wallet.address))
            jsonBal = balance.content.decode('utf-8').replace("'", '"')
            print(jsonBal)
            jsonBal = json.loads(jsonBal)
            print(type(jsonBal))
            balance_in_ltc = float(jsonBal.get('balance')) / 100000000

            if balance_in_ltc != float(user_litecoin_wallet.previous_bal):
                added_asset = float(balance_in_ltc) - float(user_litecoin_wallet.previous_bal)
                print(added_asset)
                user_litecoin_wallet.available = float(user_litecoin_wallet.available) + added_asset
                user_litecoin_wallet.previous_bal = float(user_litecoin_wallet.previous_bal) + added_asset
                user_litecoin_wallet.save()

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Litecoin Address Retrieved',
                'data': [{
                    'username': request.user.username,
                    'name': user_litecoin_wallet.name,
                    'balance': user_litecoin_wallet.available,
                    'short_name': user_litecoin_wallet.short_name,
                    'icon': user_litecoin_wallet.icon,
                    'private': user_litecoin_wallet.private_key,
                    'public': user_litecoin_wallet.public_key,
                    'address': str(user_litecoin_wallet.address),
                    'frozen': user_litecoin_wallet.frozen,
                    'amount': user_litecoin_wallet.amount,
                }]
            }
        except LitecoinWallet.DoesNotExist:
            import requests
            ltc_account_request = requests.post(
                'https://api.blockcypher.com/v1/ltc/main/addrs?token=79d9c1fb002c4543a0befb9e83d81a5c&bech32=true')
            ltc_account = ltc_account_request.content.decode('utf-8').replace("'", '"')
            print(ltc_account)
            ltc_account = json.loads(ltc_account)
            print(type(ltc_account))
            ltc_icon_url = 'https://cryptologos.cc/logos/bitcoin-btc-logo.png'

            new_ltc_wallet = LitecoinWallet.objects.create(
                user=request.user,
                name='Litecoin',
                short_name='LTC',
                icon=ltc_icon_url,
                private_key=ltc_account.get('private'),
                public_key=ltc_account.get('public'),
                address=ltc_account.get('address'),
                wif=ltc_account.get('wif'),
            )

            balance = requests.get(
                'https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance?token=79d9c1fb002c4543a0befb9e83d81a5c'.format(
                    address=ltc_account['address']))
            jsonBal = balance.content.decode('utf-8').replace("'", '"')
            jsonBal = json.loads(jsonBal)
            balance_in_ltc = float(jsonBal.get('balance')) / 100000000

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Litecoin Address Created',
                'data': [{
                    'username': request.user.username,
                    'name': new_ltc_wallet.name,
                    'balance': balance_in_ltc,
                    'short_name': new_ltc_wallet.short_name,
                    'icon': ltc_icon_url,
                    'private': new_ltc_wallet.private_key,
                    'public': new_ltc_wallet.public_key,
                    'address': str(new_ltc_wallet.address),
                    'frozen': new_ltc_wallet.frozen,
                    'amount': new_ltc_wallet.amount,
                }]
            }
        return Response(response, status=status.HTTP_200_OK)


class DashAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            import requests
            user_dash_wallet = DashWallet.objects.get(user=request.user)
            balance = requests.get(
                'https://api.blockcypher.com/v1/dash/main/addrs/{address}/balance?token=79d9c1fb002c4543a0befb9e83d81a5c'.format(
                    address=user_dash_wallet.address))
            jsonBal = balance.content.decode('utf-8').replace("'", '"')
            print(jsonBal)
            jsonBal = json.loads(jsonBal)
            print(type(jsonBal))
            balance_in_dash = float(jsonBal.get('balance')) / 100000000

            if balance_in_dash != float(user_dash_wallet.previous_bal):
                added_asset = float(balance_in_dash) - float(user_dash_wallet.previous_bal)
                print(added_asset)
                user_dash_wallet.available = float(user_dash_wallet.available) + added_asset
                user_dash_wallet.previous_bal = float(user_dash_wallet.previous_bal) + added_asset
                user_dash_wallet.save()

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Dash Address Retrieved',
                'data': [{
                    'username': request.user.username,
                    'name': user_dash_wallet.name,
                    'balance': user_dash_wallet.available,
                    'short_name': user_dash_wallet.short_name,
                    'icon': user_dash_wallet.icon,
                    'private': user_dash_wallet.private_key,
                    'public': user_dash_wallet.public_key,
                    'address': str(user_dash_wallet.address),
                    'frozen': user_dash_wallet.frozen,
                    'amount': user_dash_wallet.amount,
                }]
            }
        except DashWallet.DoesNotExist:
            import requests
            dash_account_request = requests.post(
                'https://api.blockcypher.com/v1/dash/main/addrs?token=79d9c1fb002c4543a0befb9e83d81a5c&bech32=true')
            dash_account = dash_account_request.content.decode('utf-8').replace("'", '"')
            print(dash_account)
            dash_account = json.loads(dash_account)
            print(type(dash_account))
            dash_icon_url = 'https://cryptologos.cc/logos/bitcoin-btc-logo.png'

            new_dash_wallet = DashWallet.objects.create(
                user=request.user,
                name='Dash',
                short_name='DASH',
                icon=dash_icon_url,
                private_key=dash_account.get('private'),
                public_key=dash_account.get('public'),
                address=dash_account.get('address'),
                wif=dash_account.get('wif'),
            )

            balance = requests.get(
                'https://api.blockcypher.com/v1/dash/main/addrs/{address}/balance?token=79d9c1fb002c4543a0befb9e83d81a5c'.format(
                    address=dash_account['address']))
            jsonBal = balance.content.decode('utf-8').replace("'", '"')
            jsonBal = json.loads(jsonBal)
            balance_in_dash = float(jsonBal.get('balance')) / 100000000

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Dash Address Created',
                'data': [{
                    'username': request.user.username,
                    'name': new_dash_wallet.name,
                    'balance': balance_in_dash,
                    'short_name': new_dash_wallet.short_name,
                    'icon': dash_icon_url,
                    'private': new_dash_wallet.private_key,
                    'public': new_dash_wallet.public_key,
                    'address': str(new_dash_wallet.address),
                    'frozen': new_dash_wallet.frozen,
                    'amount': new_dash_wallet.amount,
                }]
            }
        return Response(response, status=status.HTTP_200_OK)


class EthereumAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request):
        try:
            status_code = status.HTTP_200_OK
            if web3.isConnected():
                try:
                    user_ethereum_wallet = EthereumWallet.objects.get(user=request.user)
                    user_usdt_wallet = TetherUSDWallet.objects.get(user=request.user)

                    decrypted_eth_pk = web3.eth.account.decrypt(
                        keyfile_json=user_ethereum_wallet.encrypted_private_key,
                        password=request.user.username
                    )

                    hex_value = web3.toHex(decrypted_eth_pk)
                    tether_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
                    tether_abi = json.loads(
                        '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]')
                    tether_contract = web3.eth.contract(address=tether_address, abi=tether_abi)

                    print(web3.isChecksumAddress(user_ethereum_wallet.public_key))

                    balance = web3.eth.get_balance(user_ethereum_wallet.public_key)
                    balance_in_eth = web3.fromWei(balance, 'ether')
                    print(balance_in_eth)

                    if balance_in_eth != float(user_ethereum_wallet.previous_bal):
                        added_asset = float(balance_in_eth) - float(user_ethereum_wallet.previous_bal)
                        print(added_asset)
                        user_ethereum_wallet.available = float(user_ethereum_wallet.available) + added_asset
                        user_ethereum_wallet.previous_bal = float(user_ethereum_wallet.previous_bal) + added_asset
                        user_ethereum_wallet.save()

                    tether_user_address = Web3.toChecksumAddress(user_usdt_wallet.public_key)
                    tether_user_balance = tether_contract.functions.balanceOf(tether_user_address).call()
                    tether_user_balance_in_tether = web3.fromWei(tether_user_balance, 'tether')

                    if tether_user_balance_in_tether != float(user_usdt_wallet.previous_bal):
                        added_asset = float(tether_user_balance_in_tether) - float(user_usdt_wallet.previous_bal)
                        print(added_asset)
                        user_usdt_wallet.available = float(user_usdt_wallet.available) + added_asset
                        user_usdt_wallet.previous_bal = float(user_usdt_wallet.previous_bal) + added_asset
                        user_usdt_wallet.save()

                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Ethereum Address Retrieved',
                        'data': [{
                            'username': request.user.username,
                            'name': user_ethereum_wallet.name,
                            'balance': user_ethereum_wallet.available,
                            'short_name': user_ethereum_wallet.short_name,
                            'icon': user_ethereum_wallet.icon,
                            'public_address': str(user_ethereum_wallet.public_key),
                            'frozen': user_ethereum_wallet.frozen,
                            'amount': user_ethereum_wallet.amount,
                            'decrypted_private_key': str(hex_value),
                            'tether': {
                                'name': user_usdt_wallet.name,
                                'balance': user_usdt_wallet.available,
                                'short_name': user_usdt_wallet.short_name,
                                'icon': user_usdt_wallet.icon,
                                'public_address': str(user_usdt_wallet.public_key),
                                'frozen': user_usdt_wallet.frozen,
                                'amount': user_usdt_wallet.amount,
                                'decrypted_private_key': str(hex_value),
                            },
                        }]
                    }
                except EthereumWallet.DoesNotExist:
                    eth_account = web3.eth.account.create()
                    ethereum_icon_url = 'https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/116_Ethereum_logo_logos-512.png'
                    usdt_icon_url = 'https://cryptologos.cc/logos/tether-usdt-logo.png'

                    new_eth_wallet = EthereumWallet.objects.create(
                        user=request.user,
                        name='Ethereum',
                        short_name='ETH',
                        icon=ethereum_icon_url,
                        encrypted_private_key=json.dumps(eth_account.encrypt(request.user.username)),
                        public_key=eth_account.address,
                    )

                    new_usdt_wallet = TetherUSDWallet.objects.create(
                        user=request.user,
                        name='Tether USD',
                        short_name='USDT',
                        icon=usdt_icon_url,
                        encrypted_private_key=json.dumps(eth_account.encrypt(request.user.username)),
                        public_key=eth_account.address,
                    )

                    decrypted_eth_pk = web3.eth.account.decrypt(
                        keyfile_json=new_eth_wallet.encrypted_private_key,
                        password=request.user.username
                    )

                    hex_value = web3.toHex(decrypted_eth_pk)
                    balance = web3.eth.get_balance(new_eth_wallet.public_key)
                    balance_in_eth = web3.fromWei(balance, 'ether')

                    tether_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
                    tether_abi = json.loads(
                        '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]')
                    tether_contract = web3.eth.contract(address=tether_address, abi=tether_abi)
                    tether_user_address = Web3.toChecksumAddress(new_usdt_wallet.public_key)
                    tether_user_balance = tether_contract.functions.balanceOf(tether_user_address).call()
                    tether_user_balance_in_tether = web3.fromWei(tether_user_balance, 'tether')

                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Ethereum Address Created',
                        'data': [{
                            'username': request.user.username,
                            'name': new_eth_wallet.name,
                            'balance': balance_in_eth,
                            'short_name': new_eth_wallet.short_name,
                            'icon': ethereum_icon_url,
                            'public_address': str(eth_account.address),
                            'frozen': new_eth_wallet.frozen,
                            'amount': new_eth_wallet.amount,
                            'decrypted_private_key': str(hex_value),
                            'tether': {
                                'name': new_usdt_wallet.name,
                                'balance': tether_user_balance_in_tether,
                                'short_name': new_usdt_wallet.short_name,
                                'icon': new_usdt_wallet.icon,
                                'public_address': str(new_usdt_wallet.public_key),
                                'frozen': new_usdt_wallet.frozen,
                                'amount': new_usdt_wallet.amount,
                                'decrypted_private_key': str(hex_value),
                            },
                        }]
                    }
            else:
                response = {
                    'success': True,
                    'statusCode': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Not Connected To Blockchain',
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)


# Transfer Transactions On Crypto asset
class TransferEthereum(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        if not web3.isConnected():
            return Response({'message': "Not connected to blockchain"}, status=status.HTTP_403_FORBIDDEN)
        wallet_instance = EthereumWallet.objects.get(user=self.request.user)
        receiver_address = request.data.get("address", )
        amount = request.data.get("amount", )
        gas_price = float(request.data.get('networkFee', )) / 10

        decrypted_private_key = web3.eth.account.decrypt(keyfile_json=wallet_instance.encrypted_private_key,
                                                         password=request.user.username)
        nonce = web3.eth.getTransactionCount(wallet_instance.public_key)
        tx = {
            'nonce': nonce,
            'to': receiver_address,
            'value': web3.toWei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': web3.toWei('{blockchain_gasFee}'.format(blockchain_gasFee=gas_price), 'gwei')
        }

        signed_transaction = web3.eth.account.signTransaction(transaction_dict=tx, private_key=decrypted_private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        wallet_instance.previous_bal = float(wallet_instance.previous_bal) - float(amount)
        wallet_instance.available = float(wallet_instance.available) - float(amount)
        wallet_instance.save()

        return Response(
            {
                'message': "transaction successful",
                "tx_": web3.toHex(tx_hash),
                "success": bool(web3.toHex(tx_hash))
            },
            status=status.HTTP_201_CREATED
        )


class TransferOtherAsset(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        if not web3.isConnected():
            return Response({'message': "Not connected to blockchain"}, status=status.HTTP_403_FORBIDDEN)

        asset = kwargs.get('slug').upper()
        try:
            instance = BitcoinWallet.objects.get(short_name=asset, user=self.request.user)
        except BitcoinWallet.DoesNotExist:
            instance = LitecoinWallet.objects.get(short_name=asset, user=self.request.user)
        except LitecoinWallet.DoesNotExist:
            instance = DogecoinWallet.objects.get(short_name=asset, user=self.request.user)
        except DogecoinWallet.DoesNotExist:
            instance = DashWallet.objects.get(short_name=asset, user=self.request.user)
        except DashWallet.DoesNotExist:
            instance = None

        if instance:
            Klass = instance.__class__
            sender = Klass.objects.get(user=self.request.user)
            receiver_address = self.request.data.get('receiverAddress')
            print(receiver_address)
            amount = float(self.request.data.get('amount'))
            satoshi_amount = int(asset_conversion(amount, 'btc'))
            print(amount, satoshi_amount)
            # return build_transaction_and_send(
            #     sender_address=sender.address,
            #     sender_private_key=sender.private_key,
            #     sender_public_key=sender.public_key,
            #     receiver_address=receiver_address,
            #     units_in_satoshi_or_koinus=satoshi_amount,
            #     coin_symbol='btc-testnet'
            # )
        else:
            return Response({'message': 'The listed asset is not supported on our platform'}, status=status.HTTP_400_BAD_REQUEST)