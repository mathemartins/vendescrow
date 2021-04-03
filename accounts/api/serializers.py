import datetime
import phonenumbers

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django_countries.fields import Country
from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.settings import api_settings

from accounts.api.utils import expire_delta

from phonenumber_field.serializerfields import PhoneNumberField
from phonenumbers.phonenumberutil import region_code_for_country_code

from accounts.models import Profile

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('User with username and password does not exists.')
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with given email and password does not exists')
        return {
            'username': user.username,
            'token': jwt_token
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(write_only=True)
    fullName = serializers.CharField(write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        error_message=''
        fields = [
            'username',
            'fullName',
            'email',
            'phone',
            'password',
            'password2',
            'token',
            'expires',
            'message',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering. Please verify your email before continuing."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def get_token(self, obj):  # instance of the model
        user = obj
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            first_name=str(validated_data.get('fullName')).split()[0],
            last_name=str(validated_data.get('fullName')).split()[1],
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = True
        user_obj.save()

        pn = phonenumbers.parse(str(validated_data.get('phone')))
        country_affix = region_code_for_country_code(pn.country_code)
        print(country_affix)

        country_inst = Country(code=country_affix)
        print(country_inst, country_inst.name)

        profile = Profile.objects.get(user=user_obj)
        profile.phone = validated_data.get('phone')
        profile.country = country_inst
        profile.country_flag = country_inst.flag
        profile.save()

        return user_obj


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


"""
>>> person = Person(name='Chris', country='NZ')
>>> person.country
Country(code='NZ')
>>> person.country.name
'New Zealand'
>>> person.country.flag
'/static/flags/nz.gif'

{
    "username": "akapa",
    "email": "akapatemisan50@gmail.com",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNCwidXNlcm5hbWUiOiJha2FwYSIsImV4cCI6MTYxODQxOTMyMiwiZW1haWwiOiJha2FwYXRlbWlzYW41MEBnbWFpbC5jb20ifQ.phdZ3rnkBtUT-P3pFIuDRRNGudp5dVAEsd4HSgiPecE",
    "expires": "2021-04-14T16:52:02.925626Z",
    "message": "Thank you for registering. Please verify your email before continuing."
}


{
'username': 'akapa', 
'email': 'akapatemisan50@gmail.com', 
'phone': PhoneNumber(
    country_code=234, 
    national_number=9013128381, 
    extension=None, 
    italian_leading_zero=None, 
    number_of_leading_zeros=None, 
    country_code_source=1, 
    preferred_domestic_carrier_code=None
    ), 
 'password': 'pass=123'
 }
{'username': 'akapa', 'full_name': 'Akapa Temisan', 'email': 'akapatemisan50@gmail.com', 'phone': PhoneNumber(country_code=234, national_number=7010550325, extension=None, italian_leading_zero=None, number_of_leading_zeros=None, country_code_source=1, preferred_domestic_carrier_code=None), 'password': 'pass=123'}

"""
