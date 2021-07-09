from django.urls import path

from fiatwallet.api.views import EscrowWalletAPIView

urlpatterns = [
    path('<slug:slug>/details/', EscrowWalletAPIView.as_view(), name='escrow-wallet-detail'),
]
