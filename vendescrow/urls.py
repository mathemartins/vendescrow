"""vendescrow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

# base system urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='homepage'),
    path('posts/', include(('posts.urls', 'posts-url'), namespace='posts-url')),
]

# api user authentication and profile urls
urlpatterns += [
    path('api/auth/', include(('accounts.api.urls', 'api-auth'), namespace='api-auth')),
    path('api/accounts/retrieve/', include(("accounts.api.user.urls", 'accounts-api-user-url'), namespace='accounts-api-user-url')),
]

# api create wallet urls
urlpatterns += [
    path('api/wallet/', include(('wallets.api.urls', 'api-wallet'), namespace='api-wallet')),
]

# api posts urls
urlpatterns += [
    url(r'^api/posts/', include(("posts.api.urls", 'posts-api'), namespace='posts-api')),
]

# api rates urls
urlpatterns += [
    url(r'^api/fiat-rates/', include(("rates.api.urls", 'fiat_rates-api'), namespace='fiat_rates-api')),
]

# api mono account linkage
urlpatterns += [
    url(r'^api/connect-mono/', include(("mono.api.urls", 'mono_connect-api'), namespace='mono_connect-api')),
]

# api p2p urls
urlpatterns += [
    path('api/p2p/', include(('p2p.api.urls', 'api-p2p'), namespace='api-p2p')),
]

# api p2p urls
urlpatterns += [
    path('api/fiat-wallet/', include(('fiatwallet.api.urls', 'api-fiatwallet'), namespace='api-fiatwallet')),
]

# api p2p urls
urlpatterns += [
    path('api/coins/', include(('coins.api.urls', 'api-coins'), namespace='api-coins')),
]

# api referrals
urlpatterns += [
    path('api/referrals/', include(('referrals.api.urls', 'api-referrals'), namespace='api-referrals')),
]

# api create wallet urls
urlpatterns += [
    path('api/notifications/', include(('notifications.api.urls', 'api-notifications'), namespace='api-notifications')),
]

# authentication urls
urlpatterns += [
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', include(('accounts.urls', 'account-url'), namespace='account-url')),
    path('accounts/', include(("accounts.passwords.urls", 'accounts-password-url'), namespace='account-password')),
    path('accounts-reset-done/', include("accounts.passwords.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)