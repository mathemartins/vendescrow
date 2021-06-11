from django.urls import path

from .views import EthereumAddressDetailView, BitcoinAddressDetailView, TransferEthereum, LitecoinAddressDetailView, \
    DogecoinAddressDetailView, TransferOtherAsset, BitcoinWalletCallView, LitecoinWalletCallView, \
    DogecoinWalletCallView, EthereumWalletCallView, BTCLTCDOGENetworkFeeView

urlpatterns = [
    path('eth/', EthereumAddressDetailView.as_view(), name='eth-wallet'),
    path('return/eth/', EthereumWalletCallView.as_view(), name='eth-wallet-get'),

    path('btc/', BitcoinAddressDetailView.as_view(), name='bitcoin-wallet'),
    path('return/btc/', BitcoinWalletCallView.as_view(), name='bitcoin-wallet-get'),

    path('ltc/', LitecoinAddressDetailView.as_view(), name='litecoin-wallet'),
    path('return/ltc/', LitecoinWalletCallView.as_view(), name='litecoin-wallet-get'),

    path('doge/', DogecoinAddressDetailView.as_view(), name='doge-wallet'),
    path('return/doge/', DogecoinWalletCallView.as_view(), name='doge-wallet-get'),

    path('ethereum/transfer/', TransferEthereum.as_view(), name='user-transfer-wallet'),
    path('transfer/<slug:slug>/', TransferOtherAsset.as_view(), name='user-transfer-asset'),

    path('gas-fee/', BTCLTCDOGENetworkFeeView.as_view(), name='other-asset-gas'),

]
