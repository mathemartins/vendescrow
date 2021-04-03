from django.urls import path

from .views import UserDetailView, UserUpdateView

urlpatterns = [
    path('', UserDetailView.as_view(), name='user-detail'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
]
