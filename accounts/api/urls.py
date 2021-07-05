from django.urls import path

from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token # accounts app

from .views import UserLoginView, UserRegistrationView, UserLockView, FavouriteAssetAPIView

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('jwt/', obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),

    path('user-lock/', UserLockView.as_view(), name='user-update'),
    path('user-fav-coins/', FavouriteAssetAPIView.as_view(), name='fav-coin-list'),
]
