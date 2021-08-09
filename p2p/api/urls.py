from django.urls import path

from p2p.api.views import CreateP2PAPIView, DetailP2PAPIView, ListSellP2PAPIView, ListBuyP2PAPIView, \
    P2PTradeSettingsAPIView, P2PTradeSELLTransactionAPIView, P2PTradeSELLTransactionRetrieveAPIView, \
    P2PTradeBUYTransactionAPIView, P2PTradeBUYTransactionRetrieveAPIView, ModifyP2PTradeStatusAPIView, \
    P2PTradeListPerUserAPIView, P2PTradeDetailPerUserAPIView, P2PTransactionListPerUser

urlpatterns = [
    path('sell/', ListSellP2PAPIView.as_view(), name='list-sell'),
    path('buy/', ListBuyP2PAPIView.as_view(), name='list-buy'),
    path('create/', CreateP2PAPIView.as_view(), name='create'),
    path('<slug:slug>/details/', DetailP2PAPIView.as_view(), name='detail'),
    path('trade-settings/', P2PTradeSettingsAPIView.as_view(), name='p2p-trade-settings'),

    path('create/transaction/sell/', P2PTradeSELLTransactionAPIView.as_view(), name='p2p-trade-sell-create'),
    path('<slug:slug>/<slug:transaction_key>/transaction/sell/', P2PTradeSELLTransactionRetrieveAPIView.as_view(), name='p2p-sell-trade-view'),

    path('create/transaction/buy/', P2PTradeBUYTransactionAPIView.as_view(), name='p2p-buy-trade-create'),
    path('<slug:slug>/<slug:transaction_key>/transaction/buy/', P2PTradeBUYTransactionRetrieveAPIView.as_view(), name='p2p-buy-trade-view'),

    path('<slug:slug>/cancel-trade/', ModifyP2PTradeStatusAPIView.as_view(), name='p2p-user-trade-cancel'),
    path('trade-list/', P2PTradeListPerUserAPIView.as_view(), name='p2p-user-trade-list'),

    path('<slug:slug>/trade-detail/', P2PTradeDetailPerUserAPIView.as_view(), name='p2p-user-trade-detail-transaction-list'),
    path('my-transactions/', P2PTransactionListPerUser.as_view(), name='my-p2p-transactions'),
]
