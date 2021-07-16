from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from coins.api.serializers import CoinSerializer
from coins.models import Coin


class CoinListAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = CoinSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Coin.objects.all().order_by('pk')
    paginate_by = 500
