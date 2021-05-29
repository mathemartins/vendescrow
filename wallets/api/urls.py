from django.urls import path

from .views import EthereumAddressDetailView, BitcoinAddressDetailView, TransferEthereum

urlpatterns = [
    path('', EthereumAddressDetailView.as_view(), name='user-wallet'),
    path('btc/', BitcoinAddressDetailView.as_view(), name='bitcoin-wallet'),
    path('ethereum/transfer/', TransferEthereum.as_view(), name='user-transfer-wallet'),
]
