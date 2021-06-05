from django.conf.urls import url

from .views import AccountLinkageView

urlpatterns = [
    url(r'^$', AccountLinkageView.as_view(), name='account-linkage'),
]