from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from fiatwallet.api.serializers import EscrowWalletSerializer
from fiatwallet.models import FiatWallet


class EscrowWalletAPIView(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = EscrowWalletSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = FiatWallet.objects.all()

    lookup_field = ("slug",)


class EscrowWalletAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        print(kwargs)
        user_escrow_wallet_obj, created = FiatWallet.objects.get_or_create(user=self.request.user)
        status_code = status.HTTP_200_OK
        response = {
            'success': True,
            'status code': status_code,
            'message': 'Escrow wallet retrieved successfully',
            'data': [{
                'username': request.user.username,
                'firstName': request.user.first_name,
                'lastName': request.user.last_name,
                'balance': user_escrow_wallet_obj.balance,
                'account_status': user_escrow_wallet_obj.active,
                'slug': user_escrow_wallet_obj.slug
            }]
        }
        return Response(response, status=status_code)

    def post(self, request, *args, **kwargs):
        pass


