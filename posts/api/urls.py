from django.conf.urls import url

from .views import PostCreateAPIView, PostDeleteAPIView, PostDetailAPIView, PostListAPIView, PostUpdateAPIView, \
    PostDetailAPIViewV2

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^detail/$', PostDetailAPIViewV2.as_view(), name='detail-v2'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
]