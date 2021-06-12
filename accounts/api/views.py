from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.api.permissions import AnonPermissionOnly
from accounts.api.serializers import UserLoginSerializer, UserRegisterSerializer
from accounts.models import UserLock

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


class UserLockView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            user_lock_obj = UserLock.objects.get(user=self.request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status code': status_code,
                'message': 'Lock fetched successfully',
                'data': [{
                    'username': request.user.username,
                    'firstName': request.user.first_name,
                    'lastName': request.user.last_name,
                    'email': request.user.email,
                    'active': request.user.is_active,
                    'pin': str(user_lock_obj.lock_key),
                }]
            }

        except UserLock.DoesNotExist:
            UserLock.objects.create(user=self.request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status code': status.HTTP_200_OK,
                'message': 'User Lock created, please complete lock setup',
                'data': [{
                    'username': request.user.username,
                    'firstName': request.user.first_name,
                    'lastName': request.user.last_name,
                    'email': request.user.email,
                    'active': request.user.is_active,
                    'pin': '',
                }]
            }
        return Response(response, status=status_code)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        pin = data.get('pin')

        try:
            user_lock_obj = UserLock.objects.get(user=self.request.user)
            user_lock_obj.lock_key = int(pin)
            user_lock_obj.save()
            return Response({'message': 'Data Updated Successfully', 'user': str(self.request.user)}, status=201)
        except UserLock.DoesNotExist:
            UserLock.objects.create(user=self.request.user, lock_key=int(pin))
            return Response({'message': 'Data Received Successfully', 'user': str(self.request.user)}, status=201)
