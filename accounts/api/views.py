from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from accounts.api.permissions import AnonPermissionOnly
from accounts.api.serializers import UserLoginSerializer, UserRegisterSerializer


User = get_user_model()


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': True,
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly, ]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
