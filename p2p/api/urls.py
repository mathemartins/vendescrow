from django.urls import path

from p2p.api.views import CreateP2PAPIView, ListP2PAPIView, DetailP2PAPIView

urlpatterns = [
    path('', ListP2PAPIView.as_view(), name='list'),
    path('create/', CreateP2PAPIView.as_view(), name='create'),
    path('<slug:slug>/details/', DetailP2PAPIView.as_view(), name='detail'),
]
