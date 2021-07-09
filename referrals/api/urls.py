from django.urls import path

from referrals.api.views import EarlyBirdAccessAPIView

urlpatterns = [
    path('early-access/', EarlyBirdAccessAPIView.as_view(), name='early-bird-access'),
]
