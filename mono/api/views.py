import json

from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from mono.models import AccountLinkage


class AccountLinkageView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            user_account_linkage = AccountLinkage.objects.get(user=self.request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'status code': status_code,
                'message': 'linkage check successful',
                'data': [{
                    'username': request.user.username,
                    'firstName': request.user.first_name,
                    'lastName': request.user.last_name,
                    'email': request.user.email,
                    'active': request.user.is_active,
                    'monoCode': user_account_linkage.mono_code,
                    'exchangeToken': user_account_linkage.exchange_token,
                    'fullName': user_account_linkage.fullName,
                    'bank': user_account_linkage.bank,
                    'accountNumber': user_account_linkage.account_number,
                    'accountType': user_account_linkage.account_type,
                    'currency': user_account_linkage.currency,
                    'bvn': user_account_linkage.bvn
                }]
            }

        except AccountLinkage.DoesNotExist:
            status_code = status.HTTP_200_OK
            user_account_linkage = AccountLinkage.objects.create(user=self.request.user)
            response = {
                'success': True,
                'status code': status_code,
                'message': 'linkage check successful',
                'data': [{
                    'username': request.user.username,
                    'firstName': request.user.first_name,
                    'lastName': request.user.last_name,
                    'email': request.user.email,
                    'active': request.user.is_active,
                    'monoCode': user_account_linkage.mono_code,
                    'exchangeToken': user_account_linkage.exchange_token,
                    'fullName': user_account_linkage.fullName,
                    'bank': user_account_linkage.bank,
                    'accountNumber': user_account_linkage.account_number,
                    'accountType': user_account_linkage.account_type,
                    'currency': user_account_linkage.currency,
                    'bvn': user_account_linkage.bvn
                }]
            }
        return Response(response, status=status_code)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        mono_code = data.get('monoCode')

        # exchange codeId for user token details
        import requests
        url = "https://api.withmono.com/account/auth"
        payload = {"code": "{mono_connect_code}".format(mono_connect_code=mono_code)}
        headers = {"mono-sec-key": "live_sk_F4iAi3DbcMkPX5kYvRHa", "Content-Type": "application/json"}
        response = requests.request("POST", url, json=payload, headers=headers)
        response_data: dict = json.loads(response.content.decode('utf-8'))
        print(response_data)
        transaction_key = response_data.get('id')

        # fetch user information from
        url = "https://api.withmono.com/accounts/{id}".format(id=response_data.get('id'))
        headers = {"mono-sec-key": "live_sk_F4iAi3DbcMkPX5kYvRHa"}
        response = requests.request("GET", url, headers=headers)
        response_user_data: dict = json.loads(response.content.decode('utf-8'))
        print(response_user_data)

        # detailed user information
        url = "https://api.withmono.com/accounts/{id}/identity".format(id=response_data.get('id'))
        headers = {"mono-sec-key": "live_sk_F4iAi3DbcMkPX5kYvRHa"}
        response = requests.request("GET", url, headers=headers)
        response_user_detailed_data: dict = json.loads(response.content.decode('utf-8'))
        print(response_user_detailed_data)

        try:
            address_line_1 = response_user_detailed_data['addressLine1']
            address_line_2 = response_user_detailed_data['addressLine2']
        except KeyError:
            address_line_1 = "Not Available"
            address_line_2 = "Not Available"

        parsed_string_phone = response_user_detailed_data.get('phone')
        user_phone_number = parsed_string_phone if parsed_string_phone is not None else "Not Available"

        email = str(response_user_detailed_data['email'])
        bvn = str(response_user_detailed_data['bvn']),
        marital_status = str(response_user_detailed_data['maritalStatus'])
        address_line1 = str(address_line_1)
        address_line2 = str(address_line_2)
        gender = str(response_user_detailed_data['gender'])
        bank = response_user_data['account']['institution'].get('name')
        account_number = response_user_data['account'].get('accountNumber')
        account_type = response_user_data['account'].get('type')
        currency = response_user_data['account'].get('currency')
        balance_in_kobo = response_user_data['account'].get('balance')

        # create borrower for the company
        try:
            thisUser = AccountLinkage.objects.get(user=self.request.user, bvn=str(bvn[0]))
        except AccountLinkage.DoesNotExist:
            thisUser = AccountLinkage.objects.create(
                user=self.request.user,
                mono_code=mono_code,
                exchange_token=transaction_key,
                fullName=str(response_user_data['account'].get('name')),
                email=email,
                gender=gender,
                phone=user_phone_number,
                bvn=bvn[0],
                marital_status=marital_status,
                home_address=address_line1,
                office_address=address_line2,
                bank=bank,
                account_number=account_number,
                account_type=account_type,
                currency=currency,
            )
        return Response({'message': 'User Account Linked Successful!', 'exchangeToken': thisUser.exchange_token}, status=201)


