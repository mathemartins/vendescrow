from django.urls import path

from p2p.websocket.consumers import P2PTradeConsumer

ws_urlpatterns = [
    path('ws/test-path/', P2PTradeConsumer.as_asgi())
]