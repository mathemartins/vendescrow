from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from .views import UserProfileView, AccountHomeView, AccountEmailActivateView

urlpatterns = [
    path('', AccountHomeView.as_view(), name='home'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email-activate'),
    re_path(r'^email/resend-activation/$', AccountEmailActivateView.as_view(), name='resend-activation'),

    path('sign-out/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='profile'),
]
