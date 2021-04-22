from django.urls import path

from .views import PostDetailViewController

urlpatterns = [
    path('post-details/', PostDetailViewController.as_view(), name='post-details'),
]