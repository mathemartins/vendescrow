from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from referrals.models import EarlyBirdAccess
from vendescrow.utils import random_string_generator


class EarlyBirdAccessAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("https://www.vendescrow.com/")

    def post(self, request, *args, **kwargs):
        referral_code = request.query_params.get('ref_id')
        email = request.data.get('email')

        email_exists = EarlyBirdAccess.objects.filter(email=email).exists()
        referral_code_exists = EarlyBirdAccess.objects.filter(referral_code=referral_code).exists()
        if email_exists:
            return Response({'message': 'Email is already a vendecan'}, status=status.HTTP_302_FOUND)

        if referral_code_exists:
            referral_code_owner = EarlyBirdAccess.objects.get(referral_code=referral_code)
            referral_code_owner.number_of_referrals += 1
            referral_code_owner.save()

            guest_referral_code = random_string_generator(9)
            referred_guest = EarlyBirdAccess.objects.create(
                email=email,
                referral_code=guest_referral_code,
                number_of_referrals=0,
                base_url='https://api.vendescrow.com/api/referrals/early-access/?ref_id={referral_code}'.format(referral_code=guest_referral_code),
            )

            response = {
                'success': True,
                'message': 'Congratulations!, You are now a vendecan',
                'data': {
                    'email': referred_guest.email,
                    'referral_code': referred_guest.referral_code,
                    'number_of_referrals': referred_guest.number_of_referrals,
                    'referral_link': referred_guest.base_url,
                    'timestamp': referred_guest.timestamp,
                    'guests_above': EarlyBirdAccess.objects.filter(number_of_referrals__gte=referred_guest.number_of_referrals).count()
                }
            }

        else:
            guest_referral_code = random_string_generator(9)
            guest = EarlyBirdAccess.objects.create(
                email=email,
                referral_code=guest_referral_code,
                number_of_referrals=0,
                base_url='https://api.vendescrow.com/api/referrals/early-access/?ref_id={referral_code}'.format(
                    referral_code=guest_referral_code),
            )

            response = {
                'success': True,
                'message': 'Congratulations!, You are now a vendecan',
                'data': {
                    'email': guest.email,
                    'referral_code': guest.referral_code,
                    'number_of_referrals': guest.number_of_referrals,
                    'referral_link': guest.base_url,
                    'timestamp': guest.timestamp,
                    'guests_above': EarlyBirdAccess.objects.filter(number_of_referrals__gte=guest.number_of_referrals).count()
                }
            }

        return Response(response, status=status.HTTP_200_OK)
