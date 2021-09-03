import json

from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from web3 import Web3

from notifications.models import NotificationURLS
from transactions.models import Transaction
from vendescrow.blockchain.ethereum_constants import MAINNET_URL, GINACHE_URL
from vendescrow.blockchain.utils import create_address, transfer_crypto_with_sender_address, get_network_fee
from vendescrow.utils import create_notification
from wallets.models import EthereumWallet, TetherUSDWallet, BitcoinWallet, DogecoinWallet, LitecoinWallet, DashWallet

web3 = Web3(Web3.HTTPProvider(MAINNET_URL))

litecoin: str = '424f-f409-0198-4f79'
bitcoin: str = '413d-28c6-cc3c-10b3'
dogecoin: str = '2369-cce8-ec84-e3fa'
litecoin_testnet: str = 'f0c1-4225-3466-1f69'
bitcoin_testnet: str = '75c8-afcc-010a-83a5'
dogecoin_testnet: str = '2ff6-9bd9-ed93-a1b0'


class BTCLTCDOGENetworkFeeView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def post(self, request, **kwargs):
        if str(self.request.data.get('asset')) == 'btc':
            network_api = bitcoin_testnet
            receiver_address = self.request.data.get('receiverAddress')
            amount = self.request.data.get('amount')

            gas_fee = get_network_fee(crypto_network_api=network_api, receiver_address=receiver_address, amount=amount)

            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'Current Network Retrieved',
                'data': [{
                    'estimated_gas': gas_fee,
                }]
            }
            return Response(response, status=status.HTTP_201_CREATED)
        elif str(self.request.data.get('asset')) == 'ltc':
            network_api = litecoin_testnet
            receiver_address = self.request.data.get('receiverAddress')
            amount = self.request.data.get('amount')

            gas_fee = get_network_fee(crypto_network_api=network_api, receiver_address=receiver_address, amount=amount)

            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'Current Network Retrieved',
                'data': [{
                    'estimated_gas': gas_fee,
                }]
            }
            return Response(response, status=status.HTTP_201_CREATED)
        elif str(self.request.data.get('asset')) == 'doge':
            network_api = bitcoin_testnet
            receiver_address = self.request.data.get('receiverAddress')
            amount = self.request.data.get('amount')

            gas_fee = get_network_fee(crypto_network_api=network_api, receiver_address=receiver_address, amount=amount)

            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'message': 'Current Network Retrieved',
                'data': [{
                    'estimated_gas': gas_fee,
                }]
            }
            return Response(response, status=status.HTTP_201_CREATED)


class BitcoinWalletCallView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            user_bitcoin_wallet = BitcoinWallet.objects.get(user=request.user)
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
                    'short_name_btc': user_bitcoin_wallet.short_nameBTC,
                    'short_name_ltc': user_bitcoin_wallet.short_nameLTC,
                    'short_name_doge': user_bitcoin_wallet.short_nameDOGE,
                }]
            }
            return Response(response, status=status.HTTP_200_OK)
        except BitcoinWallet.DoesNotExist:
            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Bitcoin Address Retrieved',
                'data': [{
                    'username': request.user.username,
                    'name': 'Bitcoin',
                    'balance': '0',
                    'short_name': 'BTC',
                    'icon': 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                    'private': None,
                    'public': None,
                    'address': None,
                    'frozen': False,
                    'amount': '0',
                    'short_name_btc': None,
                    'short_name_ltc': None,
                    'short_name_doge': None,
                }]
            }
            return Response(response, status=status.HTTP_200_OK)


class BitcoinAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            user_bitcoin_wallet = BitcoinWallet.objects.get(user=request.user)

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
                    'short_name_btc': user_bitcoin_wallet.short_nameBTC,
                    'short_name_ltc': user_bitcoin_wallet.short_nameLTC,
                    'short_name_doge': user_bitcoin_wallet.short_nameDOGE,
                }]
            }
        except BitcoinWallet.DoesNotExist:
            btc_account = create_address(crypto_network_api=bitcoin_testnet, username=request.user.username)
            btc_icon_url = 'https://cryptologos.cc/logos/bitcoin-btc-logo.png'

            new_btc_wallet = BitcoinWallet.objects.create(
                user=request.user,
                name='Bitcoin',
                short_name='BTC',
                icon=btc_icon_url,
                private_key=btc_account.get('managed'),
                public_key=btc_account.get('managed'),
                address=btc_account['data'].get('address'),
                wif=btc_account.get('managed'),
                short_nameBTC='BTC',
            )

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Bitcoin Address Created',
                'data': [{
                    'username': request.user.username,
                    'name': new_btc_wallet.name,
                    'balance': '0',
                    'short_name': new_btc_wallet.short_name,
                    'icon': btc_icon_url,
                    'private': new_btc_wallet.private_key,
                    'public': new_btc_wallet.public_key,
                    'address': str(new_btc_wallet.address),
                    'frozen': new_btc_wallet.frozen,
                    'amount': new_btc_wallet.amount,
                    'short_name_btc': new_btc_wallet.short_nameBTC,
                    'short_name_ltc': new_btc_wallet.short_nameLTC,
                    'short_name_doge': new_btc_wallet.short_nameDOGE,
                }]
            }

            # create notification on blockio to monitor this user's address
            create_notification(
                network_key=bitcoin_testnet,
                user_endpoint=NotificationURLS.objects.get(user=request.user).url,
                address=str(new_btc_wallet.address)
            )
        return Response(response, status=status.HTTP_200_OK)


class LitecoinWalletCallView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            user_litecoin_wallet = LitecoinWallet.objects.get(user=request.user)
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
                    'short_name_btc': user_litecoin_wallet.short_nameBTC,
                    'short_name_ltc': user_litecoin_wallet.short_nameLTC,
                    'short_name_doge': user_litecoin_wallet.short_nameDOGE,
                }]
            }
            return Response(response, status=status.HTTP_200_OK)
        except LitecoinWallet.DoesNotExist:
            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Litecoin Address Retrieved',
                'data': [{
                    'username': request.user.username,
                    'name': 'Litecoin',
                    'balance': '0',
                    'short_name': 'LTC',
                    'icon': 'https://cryptologos.cc/logos/litecoin-ltc-logo.png',
                    'private': None,
                    'public': None,
                    'address': None,
                    'frozen': False,
                    'amount': '0',
                    'short_name_btc': None,
                    'short_name_ltc': None,
                    'short_name_doge': None,
                }]
            }
            return Response(response, status=status.HTTP_200_OK)


class LitecoinAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            user_litecoin_wallet = LitecoinWallet.objects.get(user=request.user)
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
                    'short_name_btc': user_litecoin_wallet.short_nameBTC,
                    'short_name_ltc': user_litecoin_wallet.short_nameLTC,
                    'short_name_doge': user_litecoin_wallet.short_nameDOGE,
                }]
            }
        except LitecoinWallet.DoesNotExist:
            ltc_account = create_address(crypto_network_api=litecoin_testnet, username=request.user.username)
            ltc_icon_url = 'https://cryptologos.cc/logos/litecoin-ltc-logo.png'

            new_ltc_wallet = LitecoinWallet.objects.create(
                user=request.user,
                name='Litecoin',
                short_name='LTC',
                icon=ltc_icon_url,
                private_key=ltc_account.get('managed'),
                public_key=ltc_account.get('managed'),
                address=ltc_account['data'].get('address'),
                wif=ltc_account.get('managed'),
                short_nameLTC='LTC'
            )

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Litecoin Address Created',
                'data': [{
                    'username': request.user.username,
                    'name': new_ltc_wallet.name,
                    'balance': '0',
                    'short_name': new_ltc_wallet.short_name,
                    'icon': ltc_icon_url,
                    'private': new_ltc_wallet.private_key,
                    'public': new_ltc_wallet.public_key,
                    'address': str(new_ltc_wallet.address),
                    'frozen': new_ltc_wallet.frozen,
                    'amount': new_ltc_wallet.amount,
                    'short_name_btc': new_ltc_wallet.short_nameBTC,
                    'short_name_ltc': new_ltc_wallet.short_nameLTC,
                    'short_name_doge': new_ltc_wallet.short_nameDOGE,
                }]
            }

            create_notification(
                network_key=litecoin_testnet,
                user_endpoint=NotificationURLS.objects.get(user=request.user).url,
                address=str(new_ltc_wallet.address)
            )

        return Response(response, status=status.HTTP_200_OK)


class DogecoinWalletCallView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            user_dogecoin_wallet = DogecoinWallet.objects.get(user=request.user)
            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Dogecoin Address Retrieved',
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
                    'short_name_btc': user_dogecoin_wallet.short_nameBTC,
                    'short_name_ltc': user_dogecoin_wallet.short_nameLTC,
                    'short_name_doge': user_dogecoin_wallet.short_nameDOGE,
                }]
            }
            return Response(response, status=status.HTTP_200_OK)
        except DogecoinWallet.DoesNotExist:
            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Dogecoin Address Retrieved',
                'data': [{
                    'username': request.user.username,
                    'name': 'Dogecoin',
                    'balance': '0',
                    'short_name': 'LTC',
                    'icon': 'https://i.imgflip.com/4w3qc7.png',
                    'private': None,
                    'public': None,
                    'address': None,
                    'frozen': False,
                    'amount': '0',
                    'short_name_btc': None,
                    'short_name_ltc': None,
                    'short_name_doge': None,
                }]
            }
            return Response(response, status=status.HTTP_200_OK)


class DogecoinAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        try:
            user_dogecoin_wallet = DogecoinWallet.objects.get(user=request.user)

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Dogecoin Address Retrieved',
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
                    'short_name_btc': user_dogecoin_wallet.short_nameBTC,
                    'short_name_ltc': user_dogecoin_wallet.short_nameLTC,
                    'short_name_doge': user_dogecoin_wallet.short_nameDOGE,
                }]
            }
        except DogecoinWallet.DoesNotExist:
            doge_account = create_address(crypto_network_api=dogecoin_testnet, username=request.user.username)
            doge_icon_url = 'https://i.imgflip.com/4w3qc7.png'

            new_doge_wallet = DogecoinWallet.objects.create(
                user=request.user,
                name='Dogecoin',
                short_name='DOGE',
                icon=doge_icon_url,
                private_key=doge_account.get('managed'),
                public_key=doge_account.get('managed'),
                address=doge_account['data'].get('address'),
                wif=doge_account.get('managed'),
                short_nameDOGE='DOGE'
            )

            response = {
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Dogecoin Address Created',
                'data': [{
                    'username': request.user.username,
                    'name': new_doge_wallet.name,
                    'balance': '0',
                    'short_name': new_doge_wallet.short_name,
                    'icon': doge_icon_url,
                    'private': new_doge_wallet.private_key,
                    'public': new_doge_wallet.public_key,
                    'address': str(new_doge_wallet.address),
                    'frozen': new_doge_wallet.frozen,
                    'amount': new_doge_wallet.amount,
                    'short_name_btc': new_doge_wallet.short_nameBTC,
                    'short_name_ltc': new_doge_wallet.short_nameLTC,
                    'short_name_doge': new_doge_wallet.short_nameDOGE,
                }]
            }

            create_notification(
                network_key=dogecoin_testnet,
                user_endpoint=NotificationURLS.objects.get(user=request.user).url,
                address=str(new_doge_wallet.address)
            )

        return Response(response, status=status.HTTP_200_OK)


class EthereumWalletCallView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request, **kwargs):
        user_ethereum_wallet = EthereumWallet.objects.get(user=request.user)
        response = {
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Ethereum Address Retrieved',
            'data': [{
                'username': request.user.username,
                'name': user_ethereum_wallet.name,
                'balance': user_ethereum_wallet.available,
                'short_name': user_ethereum_wallet.short_name,
                'icon': user_ethereum_wallet.icon,
                'private': user_ethereum_wallet.private_key,
                'public': user_ethereum_wallet.public_key,
                'address': str(user_ethereum_wallet.address),
                'frozen': user_ethereum_wallet.frozen,
                'amount': user_ethereum_wallet.amount,
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
                    tether_user_balance_in_tether = web3.fromWei(tether_user_balance, 'ether')

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
                    ethereum_icon_url = 'https://cryptologos.cc/logos/ethereum-eth-logo.png'
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


class TransferUSDTERC20(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        if not web3.isConnected():
            return Response({'message': "Not connected to blockchain"}, status=status.HTTP_403_FORBIDDEN)
        receiver_address = request.data.get("address", )
        amount = request.data.get("amount", )
        gas_price = float(request.data.get('networkFee', )) / 10

        tether_contract_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
        tether_contract_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]')
        tether_contract = web3.eth.contract(address=tether_contract_address, abi=tether_contract_abi)

        user_usdt_wallet = TetherUSDWallet.objects.get(user=request.user)
        tether_user_address = Web3.toChecksumAddress(user_usdt_wallet.public_key)

        decrypted_private_key = web3.eth.account.decrypt(keyfile_json=user_usdt_wallet.encrypted_private_key, password=request.user.username)

        nonce = web3.eth.getTransactionCount(tether_user_address)
        tx = tether_contract.functions.transfer(receiver_address, web3.toWei(amount, 'ether')).buildTransaction({
            'gas': 21000,
            'gasPrice': web3.toWei('{blockchain_gasFee}'.format(blockchain_gasFee=gas_price), 'gwei'),
            'nonce': nonce
        })
        signed_tx = web3.eth.account.signTransaction(tx, private_key=decrypted_private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

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
        print(asset)
        try:
            instance = BitcoinWallet.objects.get(short_name=asset, user=self.request.user)
        except BitcoinWallet.DoesNotExist:
            instance = LitecoinWallet.objects.get(short_name=asset, user=self.request.user)
        except LitecoinWallet.DoesNotExist:
            instance = DogecoinWallet.objects.get(short_name=asset, user=self.request.user)
        except DogecoinWallet.DoesNotExist:
            instance = None

        if not instance:
            return Response({'message': 'The listed asset is not supported on our platform'},
                            status=status.HTTP_400_BAD_REQUEST)
        print(instance)
        Klass = instance.__class__
        sender = Klass.objects.get(user=self.request.user)
        receiver_address = self.request.data.get('receiverAddress')
        amount = self.request.data.get('amount')

        if str(asset) == 'BTC':
            network = bitcoin_testnet
            vendescrow_default_address = '2N8jbkx2gfMU9vNrgHPzn9vnns3TxiEdghC'
            vend_fee = '0.00016'
            min_fee = '0.00002'

            try:
                is_vendescrow_user = Klass.objects.get(address=receiver_address)
                # send crypto

                # confirm if user have that same amount
                if float(sender.available) < float(min_fee) + float(amount):
                    raise ValueError('Cannot make transaction, insufficient balance')

                sender.available = str(round(float(sender.available) - float(amount), 8))
                is_vendescrow_user.available = str(round(float(is_vendescrow_user.available) + float(amount), 8))
                print(sender.available, is_vendescrow_user.amount)

                sender.save()
                is_vendescrow_user.save()

                # update the transaction if its between two vendescrow users
                Transaction.objects.create(
                    sender=request.user.username,
                    receiver=is_vendescrow_user.user,
                    amount=amount,
                    transaction_hash=timezone.now(),
                    asset_type=asset
                )

                try:
                    this_trx = Transaction.objects.get(receiver=vendescrow_default_address, asset_type=asset)
                    this_trx.amount = str(float(vend_fee) + float(this_trx.amount))
                    this_trx.save()
                except Transaction.DoesNotExist:
                    Transaction.objects.create(
                        receiver=vendescrow_default_address,
                        amount=vend_fee,
                        asset_type=asset
                    )
                return Response({'message': 'Transaction successful'}, status=status.HTTP_200_OK)
            except Klass.DoesNotExist:
                # send crypto outside
                if float(sender.available) < float(min_fee) + float(amount):
                    res = {
                        'message': 'Cannot make transaction, insufficient balance',
                        'trx': 'Does not exists'
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

                trx_data = transfer_crypto_with_sender_address(
                    amount=amount,
                    receiver_address=str(receiver_address),
                    crypto_network_api=network,
                )
                trx_hash = str(trx_data['data'].get('txid'))
                if str(trx_data.get('status')) == 'success':
                    sender.available = str(round(float(sender.available) - float(amount), 8))
                    sender.save()
                    response = {
                        'message': 'Transaction successful',
                        'trx': trx_hash
                    }
                    return Response(response, status=status.HTTP_200_OK)
                failed_response = {
                    'message': 'Unknown error, transaction cannot be made at this time',
                    'trx': 'Transaction id does not exists due to failed transact'
                }
                return Response(failed_response, status=status.HTTP_400_BAD_REQUEST)

        elif asset is 'LTC':
            network = litecoin_testnet
            vendescrow_default_address = 'QTeNZa6VNAEie6J5dsyhAq2Mr3TyBXEgWk'
            vend_fee = '0.0175'
            min_fee = '0.0002'

            try:
                is_vendescrow_user = Klass.objects.get(address=receiver_address)
                # send crypto

                # confirm if user have that same amount
                if float(sender.available) < float(min_fee) + float(amount):
                    raise ValueError('Cannot make transaction, insufficient balance')
                sender.available = str(round(float(sender.available) - float(amount), 8))
                is_vendescrow_user.available = str(round(float(is_vendescrow_user.available) + float(amount), 8))
                print(sender.available, is_vendescrow_user.amount)

                sender.save()
                is_vendescrow_user.save()

                # update the transaction if its between two vendescrow users
                Transaction.objects.create(
                    sender=request.user.username,
                    receiver=is_vendescrow_user.user,
                    amount=amount,
                    transaction_hash='timestamp',
                    asset_type=asset
                )

                try:
                    this_trx = Transaction.objects.get(receiver=vendescrow_default_address, asset_type=asset)
                    this_trx.amount = str(float(vend_fee) + float(this_trx.amount))
                    this_trx.save()
                except Transaction.DoesNotExist:
                    Transaction.objects.create(
                        receiver=vendescrow_default_address,
                        amount=vend_fee,
                        asset_type=asset
                    )
                return Response({'message': 'Transaction successful'}, status=status.HTTP_200_OK)
            except Klass.DoesNotExist:
                # send crypto outside
                if float(sender.available) < float(min_fee) + float(amount):
                    res = {
                        'message': 'Cannot make transaction, insufficient balance',
                        'trx': 'Does not exists'
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

                trx_data = transfer_crypto_with_sender_address(
                    amount=amount,
                    receiver_address=str(receiver_address),
                    crypto_network_api=network,
                )
                trx_hash = str(trx_data['data'].get('txid'))
                if str(trx_data.get('status')) == 'success':
                    sender.available = str(round(float(sender.available) - float(amount), 8))
                    sender.save()
                    response = {
                        'message': 'Transaction successful',
                        'trx': trx_hash
                    }
                    return Response(response, status=status.HTTP_200_OK)
                failed_response = {
                    'message': 'Unknown error, transaction cannot be made at this time',
                    'trx': 'Transaction id does not exists due to failed transact'
                }
                return Response(failed_response, status=status.HTTP_400_BAD_REQUEST)

        elif asset is 'DOGE':
            network = dogecoin_testnet
            vendescrow_default_address = '2MuRdVRRgrt6Sm2oMc4hg4Z8g1VYYpNTfcP'
            vend_fee = '9.21'
            min_fee = '2'

            try:
                is_vendescrow_user = Klass.objects.get(address=receiver_address)
                # send crypto

                # confirm if user have that same amount
                if float(sender.available) < float(min_fee) + float(amount):
                    raise ValueError('Cannot make transaction, insufficient balance')
                sender.available = str(round(float(sender.available) - float(amount), 8))
                is_vendescrow_user.available = str(round(float(is_vendescrow_user.available) + float(amount), 8))
                print(sender.available, is_vendescrow_user.amount)

                sender.save()
                is_vendescrow_user.save()

                # update the transaction if its between two vendescrow users
                Transaction.objects.create(
                    sender=request.user.username,
                    receiver=is_vendescrow_user.user,
                    amount=amount,
                    transaction_hash='timestamp',
                    asset_type=asset
                )

                try:
                    this_trx = Transaction.objects.get(receiver=vendescrow_default_address, asset_type=asset)
                    this_trx.amount = str(float(vend_fee) + float(this_trx.amount))
                    this_trx.save()
                except Transaction.DoesNotExist:
                    Transaction.objects.create(
                        receiver=vendescrow_default_address,
                        amount=vend_fee,
                        asset_type=asset
                    )
                return Response({'message': 'Transaction successful'}, status=status.HTTP_200_OK)
            except Klass.DoesNotExist:
                # send crypto outside
                if float(sender.available) < float(min_fee) + float(amount):
                    res = {
                        'message': 'Cannot make transaction, insufficient balance',
                        'trx': 'Does not exists'
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

                trx_data = transfer_crypto_with_sender_address(
                    amount=amount,
                    receiver_address=str(receiver_address),
                    crypto_network_api=network,
                )
                trx_hash = str(trx_data['data'].get('txid'))
                if str(trx_data.get('status')) == 'success':
                    sender.available = str(round(float(sender.available) - float(amount), 8))
                    sender.save()
                    response = {
                        'message': 'Transaction successful',
                        'trx': trx_hash
                    }
                    return Response(response, status=status.HTTP_200_OK)
                failed_response = {
                    'message': 'Unknown error, transaction cannot be made at this time',
                    'trx': 'Transaction id does not exists due to failed transact'
                }
                return Response(failed_response, status=status.HTTP_400_BAD_REQUEST)
