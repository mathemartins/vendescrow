from django.urls import path

from .views import EthereumAddressDetailView, BitcoinAddressDetailView, TransferEthereum, LitecoinAddressDetailView, \
    DogecoinAddressDetailView, DashAddressDetailView

urlpatterns = [
    path('', EthereumAddressDetailView.as_view(), name='user-wallet'),
    path('btc/', BitcoinAddressDetailView.as_view(), name='bitcoin-wallet'),
    path('ltc/', LitecoinAddressDetailView.as_view(), name='litecoin-wallet'),
    path('doge/', DogecoinAddressDetailView.as_view(), name='doge-wallet'),
    path('dash/', DashAddressDetailView.as_view(), name='dash-wallet'),

    path('ethereum/transfer/', TransferEthereum.as_view(), name='user-transfer-wallet'),
]
