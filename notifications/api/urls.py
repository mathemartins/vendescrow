from django.urls import path

from .views import NotificationWalletUpdate

urlpatterns = [
    path('notify/<slug:slug>/', NotificationWalletUpdate.as_view(), name='user-notification-endpoint'),

]
