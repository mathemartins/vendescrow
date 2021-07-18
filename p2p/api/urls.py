from django.urls import path

from p2p.api.views import CreateP2PAPIView, DetailP2PAPIView, ListSellP2PAPIView, ListBuyP2PAPIView, \
    P2PTradeSettingsAPIView, P2PTradeTransactionAPIView

urlpatterns = [
    path('sell/', ListSellP2PAPIView.as_view(), name='list-sell'),
    path('buy/', ListBuyP2PAPIView.as_view(), name='list-buy'),
    path('create/', CreateP2PAPIView.as_view(), name='create'),
    path('<slug:slug>/details/', DetailP2PAPIView.as_view(), name='detail'),
    path('trade-settings/', P2PTradeSettingsAPIView.as_view(), name='p2p-trade-settings'),

    path('create/transaction/', P2PTradeTransactionAPIView.as_view(), name='p2p-trade-create'),
]
