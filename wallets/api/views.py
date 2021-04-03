import json

from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from web3 import Web3

from accounts.models import Profile
from vendescrow.blockchain.ethereum_constants import MAINNET_URL
from wallets.models import Ethereum_Wallet


web3 = Web3(Web3.HTTPProvider(MAINNET_URL))


class EthereumAddressDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request):
        try:
            status_code = status.HTTP_200_OK
            if web3.isConnected():
                try:
                    user_ethereum_wallet = Ethereum_Wallet.objects.get(user=request.user)

                    decrypted_eth_pk = web3.eth.account.decrypt(
                        keyfile_json=user_ethereum_wallet.encrypted_private_key,
                        password=request.user.username
                    )

                    hex_value = web3.toHex(decrypted_eth_pk)
                    print(web3.isChecksumAddress(user_ethereum_wallet.public_key))

                    balance = web3.eth.get_balance(user_ethereum_wallet.public_key)
                    balance_in_eth = web3.fromWei(balance, 'ether')

                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Ethereum Address Retrieved',
                        'data': [{
                            'username': request.user.username,
                            'name': user_ethereum_wallet.name,
                            'balance': balance_in_eth,
                            'short_name': user_ethereum_wallet.short_name,
                            'icon': user_ethereum_wallet.icon,
                            'public_address': str(user_ethereum_wallet.public_key),
                            'frozen': user_ethereum_wallet.frozen,
                            'amount': user_ethereum_wallet.amount,
                            'decrypted_private_key': str(hex_value)
                        }]
                    }
                except Ethereum_Wallet.DoesNotExist:
                    eth_account = web3.eth.account.create()
                    ethereum_icon_url = 'https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/116_Ethereum_logo_logos-512.png'

                    new_eth_wallet = Ethereum_Wallet.objects.create(
                        user=request.user,
                        name='Ethereum',
                        short_name='ETH',
                        icon=ethereum_icon_url,
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
                            'decrypted_private_key':str(hex_value)
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