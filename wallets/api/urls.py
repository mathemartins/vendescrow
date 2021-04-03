from django.urls import path

from .views import EthereumAddressDetailView

urlpatterns = [
    path('', EthereumAddressDetailView.as_view(), name='user-wallet'),
]
