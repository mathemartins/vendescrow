from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Profile


class UserDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]

    def get(self, request):
        try:
            user_profile_obj = Profile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'username': request.user.username,
                    'firstName': request.user.first_name,
                    'lastName': request.user.last_name,
                    'email': request.user.email,
                    'active': request.user.is_active,
                    'keycode': user_profile_obj.keycode,
                    'phoneNumber': user_profile_obj.get_phone(),
                    'ssn': user_profile_obj.ssn,
                    'slug': user_profile_obj.slug,
                    'country': user_profile_obj.get_country(),
                    'country_flag': user_profile_obj.country_flag
                }]
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)


class UserUpdateView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        ssn = data.get('ssn', )

        user_profile_obj = Profile.objects.get(user=self.request.user)
        user_profile_obj.ssn = ssn
        user_profile_obj.save()

        return Response({'message': 'Data Received Successfully'}, status=201)