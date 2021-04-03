from django.conf.urls import url

from .views import FiatRateAPIView

urlpatterns = [
    url(r'^$', FiatRateAPIView.as_view(), name='list'),
]