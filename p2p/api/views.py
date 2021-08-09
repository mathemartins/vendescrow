import datetime
import json
import os

import requests

from django.db.models import Q
from django.template.loader import get_template
from django.utils import timezone
from pymono import Mono
from rest_framework import mixins, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from web3 import Web3

from fiatwallet.models import FiatWallet, WalletTransactionsHistory
from mono.models import AccountLinkage
from p2p.api.serializers import P2PTradeSerializer, P2PTransactionSerializer
from p2p.models import P2PTrade, P2PTradeCoreSettings, P2PTransaction
from vendescrow import email_settings
from vendescrow.utils import round_decimals_down, unique_id_generator, random_string_generator
from wallets.api.views import web3
from wallets.models import BitcoinWallet, LitecoinWallet, DogecoinWallet, EthereumWallet, TetherUSDWallet


class ListCreateP2PAPIView(mixins.CreateModelMixin, ListAPIView):  # DetailView CreateView FormView
    lookup_field = 'slug'
    serializer_class = P2PTradeSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        qs = P2PTrade.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(max_trading_amount_in_fiat__icontains=query) | Q(
                min_trading_amount_in_fiat__icontains=query)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(trade_creator=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class CreateP2PAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data

        parsed_creator_rate = round_decimals_down(float(data.get('creatorDollarRate')))

        P2PTrade.objects.create(
            trade_creator=request.user,
            trade_listed_as=data.get('tradeListedAs'),
            creator_rate_in_dollar=parsed_creator_rate,
            crypto_trading_amount=data.get('unitsOfCryptoSelectedForTrade'),
            min_trading_amount_in_fiat=data.get('lowestOrderLimit'),
            max_trading_amount_in_fiat=data.get('highestOrderLimit'),
            asset_to_trade=data.get('asset'),
            price_slippage=data.get('priceSlippage'),
        )
        return Response({'message': 'Trade Created Successfully'}, status=201)


class ListSellP2PAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = P2PTradeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 500

    def get_queryset(self):
        try:
            viewer_username = P2PTrade.objects.get(trade_creator=self.request.user, active=True)
            return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
                active=True).filter(trade_listed_as="I WANT TO SELL").filter(owner_cancel_trade=False).exclude(
                trade_creator__username=viewer_username).order_by('?')
        except P2PTrade.DoesNotExist:
            return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
                active=True).filter(trade_listed_as="I WANT TO SELL").filter(owner_cancel_trade=False).order_by('?')


class ListBuyP2PAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = P2PTradeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 500

    def get_queryset(self):
        try:
            viewer_username = P2PTrade.objects.get(trade_creator=self.request.user, active=True)
            return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
                active=True).filter(trade_listed_as="I WANT TO BUY").filter(owner_cancel_trade=False).exclude(
                trade_creator__username=viewer_username).order_by('?')
        except P2PTrade.DoesNotExist:
            return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
                active=True).filter(trade_listed_as="I WANT TO BUY").filter(owner_cancel_trade=False).order_by('?')


class DetailP2PAPIView(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = P2PTradeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        viewer_username = P2PTrade.objects.get(trade_creator=self.request.user, active=True).trade_creator.username
        return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
            active=True).filter(owner_cancel_trade=False).exclude(trade_creator__username=viewer_username)

    def get_object(self):
        slug = self.kwargs["slug"]
        return get_object_or_404(P2PTrade, slug=slug)


class P2PTradeSettingsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_escrow_fee_obj = P2PTradeCoreSettings.objects.all().first()
        status_code = status.HTTP_200_OK
        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'Vendescrow settings retrieved successfully',
            'data': [{
                'escrow_fee': user_escrow_fee_obj.escrow_fee,
            }]
        }
        return Response(response, status=status_code)


class P2PTradeSELLTransactionRetrieveAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, *args, **kwargs):
        print(kwargs)
        trade_instance = P2PTrade.objects.get(slug=kwargs.get('slug'))
        transaction_key = kwargs.get('transaction_key')
        user_transaction_instance = P2PTransaction.objects.get(trade=trade_instance, trade_visitor=request.user,
                                                               transaction_key=transaction_key)
        status_code = status.HTTP_200_OK
        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'Transaction Trade retrieved successfully',
            'data': [{
                'transaction_key': user_transaction_instance.transaction_key,
                'trade_visitor': user_transaction_instance.trade_visitor.username,
                'units_of_asset': user_transaction_instance.crypto_unit_transacted,
                'fiat_paid': user_transaction_instance.fiat_paid,
                'bank': trade_instance.trade_creator.accountlinkage.bank.capitalize(),
                'account_number': trade_instance.trade_creator.accountlinkage.account_number,
                'account_name': trade_instance.trade_creator.accountlinkage.fullName,
                'status': user_transaction_instance.status,
                'slug': user_transaction_instance.transaction_key,
            }]
        }
        return Response(response, status=status_code)


class P2PTradeSELLTransactionAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def post(self, request, *args, **kwargs):
        data = request.data
        ACTION_CANCELLED = 0
        ACTION_CREATE = 1
        ACTION_APPEAL = 2
        ACTION_VERIFY_TRANSACTION = 3

        if data['actionType'] == ACTION_CREATE:
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            trade_customer = request.user
            trade_identifier = unique_id_generator(trade_instance)
            transaction_obj = P2PTransaction.objects.create(
                trade=trade_instance,
                transaction_key=trade_identifier,
                trade_visitor=trade_customer,
                crypto_unit_transacted=data['unitsOfAsset'],
                fiat_paid=data['fiatToBePaid'],
                status=data['status'],
                slug=trade_identifier,
            )

            # set trade inactive until transaction is completed
            trade_instance.active = False
            trade_instance.transactions += 1
            trade_instance.save()

            # send email to trade owner notifying them about their trade
            context = {
                'seller': trade_instance.trade_creator.first_name,
                'buyer': "{first_name} {last_name}".format(first_name=request.user.first_name,
                                                           last_name=request.user.last_name),
                'tradeType': "SELL {asset}".format(asset=trade_instance.asset_to_trade),
                'currency': data['currency'],
                'amount': transaction_obj.fiat_paid,
                'narration': trade_identifier
            }
            html_ = get_template("p2p/emails/p2pTradeSellerEmail.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [trade_instance.trade_creator.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            # send email to trade owner notifying them about their trade

            context = {
                'seller': "{first_name} {last_name}".format(first_name=trade_instance.trade_creator.first_name,
                                                            last_name=trade_instance.trade_creator.last_name),
                'buyer': request.user,
                'tradeType': "BUY {asset}".format(asset=trade_instance.asset_to_trade),
                'amount': transaction_obj.fiat_paid,
                'currency': data['currency'],
                'narration': trade_identifier,
                'seller_bank': trade_instance.trade_creator.accountlinkage.bank.capitalize(),
                'seller_account_number': trade_instance.trade_creator.accountlinkage.account_number,
                'seller_name': trade_instance.trade_creator.accountlinkage.fullName
            }

            html_ = get_template("p2p/emails/p2pTradeBuyerEmail.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            return Response({'message': 'Trade Transaction Created Successfully',
                             'tradeNarration': '{narration}'.format(narration=trade_identifier),
                             'statusCode': status.HTTP_201_CREATED}, status=201)

        elif data['actionType'] == ACTION_CANCELLED:
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            trade_customer = request.user
            transaction_instance = P2PTransaction.objects.get(transaction_key=data['transactionKey'],
                                                              trade_visitor=trade_customer, trade=trade_instance)
            transaction_instance.status = "CANCELLED"
            transaction_instance.save()

            # activate the trade again
            trade_instance.active = True
            trade_instance.save()

            # send email notifying both parties trade has been cancelled
            context = {
                'seller': trade_instance.trade_creator.first_name,
                'buyer': "{first_name} {last_name}".format(first_name=request.user.first_name,
                                                           last_name=request.user.last_name),
                'tradeType': "SELL {asset}".format(asset=trade_instance.asset_to_trade),
                'narration': transaction_instance.transaction_key
            }
            html_ = get_template("p2p/emails/p2pTradeCancelledSeller.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [trade_instance.trade_creator.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            # notify buyer that they cancelled
            context = {
                'buyer': request.user.username,
                'tradeType': "SELL {asset}".format(asset=trade_instance.asset_to_trade),
                'narration': transaction_instance.transaction_key
            }
            html_ = get_template("p2p/emails/p2pTradeCancelledBuyer.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            return Response({'message': 'Trade Transaction Cancelled Successfully', 'statusCode': status.HTTP_200_OK},
                            status=201)

        elif data['actionType'] == ACTION_APPEAL:
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            trade_customer = request.user
            transaction_instance = P2PTransaction.objects.get(transaction_key=data['transactionKey'],
                                                              trade_visitor=trade_customer, trade=trade_instance)
            transaction_instance.status = "ON_APPEAL"
            transaction_instance.save()

            # do not activate the trade again, until resolved
            trade_instance.active = False
            trade_instance.save()

            # send email notifying both parties trade has been set on_appeal
            context = {
                'seller': trade_instance.trade_creator.first_name,
                'buyer': "{first_name} {last_name}".format(first_name=request.user.first_name,
                                                           last_name=request.user.last_name),
                'tradeType': "SELL {asset}".format(asset=trade_instance.asset_to_trade),
                'currency': data['currency'],
                'amount': transaction_instance.fiat_paid,
                'narration': transaction_instance.transaction_key,
                'phone': request.user.profile.phone
            }
            html_ = get_template("p2p/emails/p2pTradeOnAppealSeller.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [trade_instance.trade_creator.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            # notify buyer that they cancelled
            context = {
                'seller': trade_instance.trade_creator.first_name,
                'buyer': request.user.username,
                'tradeType': "SELL {asset}".format(asset=trade_instance.asset_to_trade),
                'narration': transaction_instance.transaction_key,
                'currency': data['currency'],
                'amount': transaction_instance.fiat_paid,
                'phone': trade_instance.trade_creator.profile.phone
            }
            html_ = get_template("p2p/emails/p2pTradeOnAppealBuyer.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            return Response({'message': 'Trade Transaction Has Been Placed On Appeal Successfully',
                             'statusCode': status.HTTP_200_OK}, status=201)

        elif data['actionType'] == ACTION_VERIFY_TRANSACTION:
            asset = data['asset']
            escrow_instance = P2PTradeCoreSettings.objects.all().first()
            seller = P2PTransaction.objects.get(transaction_key=data['transactionKey']).trade.trade_creator
            buyer = request.user
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            transaction_instance = P2PTransaction.objects.get(
                transaction_key=data['transactionKey'],
                trade_visitor=buyer,
                trade=trade_instance
            )

            print(AccountLinkage.objects.get(user=buyer).exchange_token)

            # get latest data through data_sync for buyer
            url = "https://api.withmono.com/accounts/{exchange_token}/sync".format(
                exchange_token=AccountLinkage.objects.get(user=buyer).exchange_token)
            headers = {
                "Accept": "application/json",
                "mono-sec-key": "live_sk_8vrj5erb1rlMwvLzQgot"
            }
            response = requests.request("POST", url, headers=headers)
            response_data_sync = json.loads(response.content.decode('utf-8'))
            print(response_data_sync)

            # get latest data through data_sync for seller
            url = "https://api.withmono.com/accounts/{exchange_token}/sync".format(
                exchange_token=AccountLinkage.objects.get(user=seller).exchange_token)
            headers = {
                "Accept": "application/json",
                "mono-sec-key": "live_sk_8vrj5erb1rlMwvLzQgot"
            }
            response = requests.request("POST", url, headers=headers)
            response_data_sync = json.loads(response.content.decode('utf-8'))
            print(response_data_sync)

            # check debit transaction list for buyer
            url = "https://api.withmono.com/accounts/{exchange_token}/transactions".format(
                exchange_token=AccountLinkage.objects.get(user=buyer).exchange_token)
            querystring = {"type": "debit"}
            headers = {
                "Accept": "application/json",
                "mono-sec-key": "live_sk_8vrj5erb1rlMwvLzQgot"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            response_data_buyer = json.loads(response.content.decode('utf-8'))
            print(response_data_buyer)

            data_list = response_data_buyer['data']
            status_code = status.HTTP_200_OK

            for index in range(len(data_list)):
                for key in data_list[index]:
                    print(data_list[index]['narration'])
                    narration = data_list[index]['narration']
                    amount: int = data_list[index]['amount'] / 100
                    date: str = data_list[index]['date']
                    print(date)
                    today = datetime.date.today()
                    date_list = list()
                    date_list.append(today)
                    this_day = str(date_list[0])
                    print(this_day)
                    if narration.find(AccountLinkage.objects.get(
                            user=buyer).fullName) and amount == transaction_instance.fiat_paid and this_day in date:
                        print("found!")
                        # check seller account immediately

                        # check credit transaction list for seller
                        url = "https://api.withmono.com/accounts/{exchange_token}/transactions".format(
                            exchange_token=AccountLinkage.objects.get(user=seller).exchange_token)
                        querystring = {"type": "credit"}
                        headers = {
                            "Accept": "application/json",
                            "mono-sec-key": "live_sk_8vrj5erb1rlMwvLzQgot"
                        }
                        response = requests.request("GET", url, headers=headers, params=querystring)
                        response_data_seller = json.loads(response.content.decode('utf-8'))
                        print(response_data_seller['data'])

                        data_list = response_data_seller['data']
                        status_code = status.HTTP_200_OK
                        for index in range(len(data_list)):
                            for key in data_list[index]:
                                print(data_list[index]['narration'])
                                narration = data_list[index]['narration']
                                amount: int = data_list[index]['amount'] / 100
                                date: str = data_list[index]['date']
                                print(date)
                                if narration.find(AccountLinkage.objects.get(
                                        user=seller).fullName) and amount == transaction_instance.fiat_paid and this_day in date:
                                    print("found!")
                                    if asset == 'BTC':
                                        seller = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = BitcoinWallet.objects.get(user=buyer)
                                        seller_wallet = BitcoinWallet.objects.get(user=seller)

                                        # send crypto to buyer and reduce frozen asset of seller
                                        seller_wallet.amount = str(round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        buyer_wallet.available = str(round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        seller_wallet.save()
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # record transactions on wallet for buyer and seller
                                        buyer_wallet_trx = WalletTransactionsHistory.objects.create(
                                            wallet=buyer_escrow_wallet,
                                            transaction_type='Debit',
                                            amount=float(escrow_instance.escrow_fee),
                                            transaction_key=random_string_generator(15),
                                            slug=random_string_generator()
                                        )

                                        seller_wallet_trx = WalletTransactionsHistory.objects.create(
                                            wallet=seller_escrow_wallet,
                                            transaction_type='Debit',
                                            amount=float(escrow_instance.escrow_fee),
                                            transaction_key=random_string_generator(15),
                                            slug=random_string_generator()
                                        )

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name,
                                                                                        last_name=seller.last_name),
                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = buyer
                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )
                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": timezone.now(),
                                                "success": bool(timezone.now())
                                            },
                                            status=status.HTTP_201_CREATED
                                        )
                                    elif asset == 'LTC':
                                        seller = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = LitecoinWallet.objects.get(user=buyer)
                                        seller_wallet = LitecoinWallet.objects.get(user=seller)

                                        # send crypto to buyer and reduce frozen asset of seller
                                        seller_wallet.amount = str(
                                            round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        buyer_wallet.available = str(
                                            round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))

                                        seller_wallet.save()
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name,
                                                                                        last_name=seller.last_name),
                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = buyer
                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )
                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": timezone.now(),
                                                "success": bool(timezone.now())
                                            },
                                            status=status.HTTP_201_CREATED
                                        )
                                    elif asset == 'DOGE':
                                        seller = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = DogecoinWallet.objects.get(user=self.request.user)
                                        seller_wallet = DogecoinWallet.objects.get(user=seller)
                                        seller_wallet.amount = str(
                                            round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        buyer_wallet.available = str(
                                            round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        seller_wallet.save()
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name,
                                                                                        last_name=seller.last_name),
                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = buyer
                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )
                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": timezone.now(),
                                                "success": bool(timezone.now())
                                            },
                                            status=status.HTTP_201_CREATED
                                        )
                                    elif asset == 'ETH':
                                        seller = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = EthereumWallet.objects.get(user=buyer)
                                        seller_wallet = EthereumWallet.objects.get(user=seller)

                                        # transfer crypto to buyer
                                        receiver_address = buyer_wallet.public_key
                                        amount = data['cryptoUnits']
                                        gas_price = float(data['networkFee']) / 10

                                        decrypted_private_key = web3.eth.account.decrypt(
                                            keyfile_json=seller_wallet.encrypted_private_key,
                                            password=seller.username)

                                        nonce = web3.eth.getTransactionCount(seller_wallet.public_key)
                                        tx = {
                                            'nonce': nonce,
                                            'to': receiver_address,
                                            'value': web3.toWei(amount, 'ether'),
                                            'gas': 21000,
                                            'gasPrice': web3.toWei(
                                                '{blockchain_gasFee}'.format(blockchain_gasFee=gas_price),
                                                'gwei')
                                        }

                                        signed_transaction = web3.eth.account.signTransaction(transaction_dict=tx,
                                                                                              private_key=decrypted_private_key)
                                        tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
                                        seller_wallet.amount = str(
                                            round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        seller_wallet.previous_bal = str(
                                            round(float(seller_wallet.previous_bal) - float(data['cryptoUnits']), 8))
                                        seller_wallet.save()

                                        buyer_wallet.available = str(
                                            round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        buyer_wallet.previous_bal = str(
                                            round(float(buyer_wallet.previous_bal) + float(data['cryptoUnits']), 8))
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name,
                                                                                        last_name=seller.last_name),
                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = buyer
                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )
                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": web3.toHex(tx_hash),
                                                "success": bool(web3.toHex(tx_hash))
                                            },
                                            status=status.HTTP_201_CREATED
                                        )
                                    elif asset == 'USDT':
                                        seller = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = EthereumWallet.objects.get(user=buyer)
                                        seller_wallet = EthereumWallet.objects.get(user=seller)

                                        seller_wallet.amount = str(
                                            round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        buyer_wallet.available = str(
                                            round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))

                                        receiver_address = buyer_wallet.public_key

                                        amount = data['cryptoUnits']
                                        gas_price = float(request.data.get('networkFee', )) / 10

                                        tether_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
                                        tether_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]')
                                        tether_contract = web3.eth.contract(address=tether_address, abi=tether_abi)

                                        user_usdt_wallet = TetherUSDWallet.objects.get(user=seller)
                                        tether_user_address = Web3.toChecksumAddress(user_usdt_wallet.public_key)

                                        decrypted_private_key = web3.eth.account.decrypt(
                                            keyfile_json=user_usdt_wallet.encrypted_private_key,
                                            password=seller.username)

                                        nonce = web3.eth.getTransactionCount(tether_user_address)
                                        tx = tether_contract.functions.transfer(
                                            receiver_address,
                                            web3.toWei(amount, 'ether')).buildTransaction({
                                            'gas': 21000,
                                            'gasPrice': web3.toWei(
                                                '{blockchain_gasFee}'.format(blockchain_gasFee=gas_price), 'gwei'),
                                            'nonce': nonce
                                        })
                                        signed_tx = web3.eth.account.signTransaction(tx,private_key=decrypted_private_key)
                                        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

                                        seller_wallet.amount = str(
                                            round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        seller_wallet.previous_bal = str(
                                            round(float(seller_wallet.previous_bal) - float(data['cryptoUnits']), 8))
                                        seller_wallet.save()

                                        buyer_wallet.available = str(
                                            round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        buyer_wallet.previous_bal = str(
                                            round(float(buyer_wallet.previous_bal) + float(data['cryptoUnits']), 8))
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(
                                            escrow_instance.escrow_fee)
                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name,
                                                                                        last_name=seller.last_name),
                                            'buyer': request.user.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': request.user.profile.phone
                                        }
                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [request.user.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = request.user
                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )
                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": web3.toHex(tx_hash),
                                                "success": bool(web3.toHex(tx_hash))
                                            },
                                            status=status.HTTP_201_CREATED
                                        )
                                return Response(response, status=status_code)

                    return Response({"message": "Transaction not found"}, status=status_code)


class P2PTradeBUYTransactionRetrieveAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, *args, **kwargs):
        print(kwargs)
        trade_instance = P2PTrade.objects.get(slug=kwargs.get('slug'))
        transaction_key = kwargs.get('transaction_key')
        user_transaction_instance = P2PTransaction.objects.get(trade=trade_instance, trade_visitor=request.user,
                                                               transaction_key=transaction_key)
        status_code = status.HTTP_200_OK
        response = {
            'success': True,
            'statusCode': status_code,
            'message': 'Transaction Trade retrieved successfully',
            'data': [{
                'transaction_key': user_transaction_instance.transaction_key,
                'trade_visitor': user_transaction_instance.trade_visitor.username,
                'units_of_asset': user_transaction_instance.crypto_unit_transacted,
                'fiat_paid': user_transaction_instance.fiat_paid,
                'bank': trade_instance.trade_creator.accountlinkage.bank.capitalize(),
                'account_number': trade_instance.trade_creator.accountlinkage.account_number,
                'account_name': trade_instance.trade_creator.accountlinkage.fullName,
                'status': user_transaction_instance.status,
                'slug': user_transaction_instance.transaction_key,
            }]
        }
        return Response(response, status=status_code)


class P2PTradeBUYTransactionAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def post(self, request, *args, **kwargs):
        data = request.data
        ACTION_CANCELLED = 0
        ACTION_CREATE = 1
        ACTION_APPEAL = 2
        ACTION_VERIFY_TRANSACTION = 3

        if data['actionType'] == ACTION_CREATE:
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            trade_visitor = request.user
            trade_identifier = unique_id_generator(trade_instance)
            transaction_obj = P2PTransaction.objects.create(
                trade=trade_instance,
                transaction_key=trade_identifier,
                trade_visitor=trade_visitor,
                crypto_unit_transacted=data['unitsOfAsset'],
                fiat_paid=data['fiatToBePaid'],
                status=data['status'],
                slug=trade_identifier,
            )

            # set trade inactive until transaction is completed
            trade_instance.active = False
            trade_instance.transactions += 1
            trade_instance.save()

            # send email to trade owner notifying them about their trade
            context = {
                'seller': trade_visitor.first_name,
                'buyer': "{first_name} {last_name}".format(first_name=trade_instance.trade_creator.first_name,
                                                           last_name=trade_instance.trade_creator.last_name),
                'tradeType': "BUY {asset}".format(asset=trade_instance.asset_to_trade),
                'currency': data['currency'],
                'amount': transaction_obj.fiat_paid,
                'narration': trade_identifier
            }
            html_ = get_template("p2p/emails/p2pTradeSellerEmail.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [trade_instance.trade_creator.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            # send email to trade visitor notifying them about the trade
            context = {
                'seller': trade_visitor.first_name,
                'buyer': "{first_name} {last_name}".format(first_name=trade_instance.trade_creator.first_name,
                                                           last_name=trade_instance.trade_creator.last_name),
                'tradeType': "SELL {asset}".format(asset=trade_instance.asset_to_trade),
                'amount': transaction_obj.fiat_paid,
                'currency': data['currency'],
                'narration': trade_identifier,
                'seller_bank': trade_visitor.accountlinkage.bank.capitalize(),
                'seller_account_number': trade_visitor.accountlinkage.account_number,
                'seller_name': trade_visitor.accountlinkage.fullName
            }

            html_ = get_template("p2p/emails/p2pTradeBuyerEmail.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            return Response({'message': 'Trade Transaction Created Successfully',
                             'tradeNarration': '{narration}'.format(narration=trade_identifier),
                             'statusCode': status.HTTP_201_CREATED}, status=201)

        elif data['actionType'] == ACTION_CANCELLED:
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            trade_visitor = request.user
            transaction_instance = P2PTransaction.objects.get(transaction_key=data['transactionKey'],
                                                              trade_visitor=trade_visitor, trade=trade_instance)
            transaction_instance.status = "CANCELLED"
            transaction_instance.save()

            # activate the trade again
            trade_instance.active = True
            trade_instance.save()

            # send email notifying both parties trade has been cancelled
            context = {
                'seller': trade_visitor.first_name,
                'buyer': "{first_name} {last_name}".format(first_name=trade_instance.trade_creator.first_name,
                                                           last_name=trade_instance.trade_creator.last_name),
                'tradeType': "BUY {asset}".format(asset=trade_instance.asset_to_trade),
                'narration': transaction_instance.transaction_key
            }
            html_ = get_template("p2p/emails/p2pTradeCancelledSeller.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [trade_instance.trade_creator.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            # notify seller that they cancelled
            context = {
                'buyer': trade_instance.trade_creator.username,
                'tradeType': "BUY {asset}".format(asset=trade_instance.asset_to_trade),
                'narration': transaction_instance.transaction_key
            }
            html_ = get_template("p2p/emails/p2pTradeCancelledBuyer.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            return Response({'message': 'Trade Transaction Cancelled Successfully', 'statusCode': status.HTTP_200_OK},
                            status=201)

        elif data['actionType'] == ACTION_APPEAL:
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            trade_visitor = request.user
            transaction_instance = P2PTransaction.objects.get(transaction_key=data['transactionKey'],
                                                              trade_visitor=trade_visitor, trade=trade_instance)
            transaction_instance.status = "ON_APPEAL"
            transaction_instance.save()

            # activate the trade again
            trade_instance.active = False
            trade_instance.save()

            # send email notifying both parties trade has been set on_appeal
            context = {
                'seller': trade_visitor.first_name,
                'buyer': "{first_name} {last_name}".format(first_name=trade_instance.trade_creator.first_name,
                                                           last_name=trade_instance.trade_creator.last_name),
                'tradeType': "BUY {asset}".format(asset=trade_instance.asset_to_trade),
                'currency': data['currency'],
                'amount': transaction_instance.fiat_paid,
                'narration': transaction_instance.transaction_key,
                'phone': request.user.profile.phone
            }
            html_ = get_template("p2p/emails/p2pTradeOnAppealSeller.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [trade_instance.trade_creator.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            # notify buyer that they cancelled
            context = {
                'seller': trade_visitor.first_name,
                'buyer': trade_instance.trade_creator.username,
                'tradeType': "BUY {asset}".format(asset=trade_instance.asset_to_trade),
                'narration': transaction_instance.transaction_key,
                'currency': data['currency'],
                'amount': transaction_instance.fiat_paid,
                'phone': trade_instance.trade_creator.profile.phone
            }
            html_ = get_template("p2p/emails/p2pTradeOnAppealBuyer.html").render(context)
            subject = 'Vendescrow P2P Trade'
            from_email = email_settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = False
            message.send()

            return Response({'message': 'Trade Transaction Has Been Placed On Appeal Successfully',
                             'statusCode': status.HTTP_200_OK}, status=201)

        elif data['actionType'] == ACTION_VERIFY_TRANSACTION:
            asset = data['asset']
            escrow_instance = P2PTradeCoreSettings.objects.all().first()
            buyer = P2PTransaction.objects.get(transaction_key=data['transactionKey']).trade.trade_creator
            seller = request.user
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            transaction_instance = P2PTransaction.objects.get(
                transaction_key=data['transactionKey'],
                trade_visitor=seller,
                trade=trade_instance
            )

            # get latest data through data_sync for buyer
            url = "https://api.withmono.com/accounts/{exchange_token}/sync".format(
                exchange_token=AccountLinkage.objects.get(user=buyer).exchange_token)
            headers = {
                "Accept": "application/json",
                "mono-sec-key": "live_sk_8vrj5erb1rlMwvLzQgot"
            }

            response = requests.request("POST", url, headers=headers)
            response_data_sync = json.loads(response.content.decode('utf-8'))
            print(response_data_sync)

            # get latest data through data_sync for seller
            url = "https://api.withmono.com/accounts/{exchange_token}/sync".format(
                exchange_token=AccountLinkage.objects.get(user=seller).exchange_token)
            headers = {
                "Accept": "application/json",
                "mono-sec-key": "live_sk_8vrj5erb1rlMwvLzQgot"
            }

            response = requests.request("POST", url, headers=headers)
            response_data_sync = json.loads(response.content.decode('utf-8'))
            print(response_data_sync)

            # check debit transaction list for buyer
            url = "https://api.withmono.com/accounts/{exchange_token}/transactions".format(
                exchange_token=AccountLinkage.objects.get(user=buyer).exchange_token)
            querystring = {"type": "debit"}

            headers = {
                "Accept": "application/json",
                "mono-sec-key": "live_sk_8vrj5erb1rlMwvLzQgot"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            response_data_buyer = json.loads(response.content.decode('utf-8'))
            print(response_data_buyer)

            data_list = response_data_buyer['data']
            status_code = status.HTTP_200_OK

            for index in range(len(data_list)):
                for key in data_list[index]:
                    print(data_list[index]['narration'])
                    narration = data_list[index]['narration']
                    amount: int = data_list[index]['amount'] / 100
                    date: str = data_list[index]['date']
                    print(date)
                    today = datetime.date.today()
                    date_list = list()
                    date_list.append(today)
                    this_day = str(date_list[0])
                    print(this_day)
                    if narration.find(AccountLinkage.objects.get(user=buyer).fullName) and amount == transaction_instance.fiat_paid and this_day in date:
                        print("found!")
                        # check seller account immediately
                        # check credit transaction list for seller
                        url = "https://api.withmono.com/accounts/{exchange_token}/transactions".format(
                            exchange_token=AccountLinkage.objects.get(user=seller).exchange_token)
                        querystring = {"type": "credit"}
                        headers = {
                            "Accept": "application/json",
                            "mono-sec-key": "live_sk_8vrj5erb1rlMwvLzQgot"
                        }

                        response = requests.request("GET", url, headers=headers, params=querystring)
                        response_data_seller = json.loads(response.content.decode('utf-8'))
                        print(response_data_seller['data'])
                        data_list = response_data_seller['data']
                        status_code = status.HTTP_200_OK
                        for index in range(len(data_list)):
                            for key in data_list[index]:
                                print(data_list[index]['narration'])
                                narration = data_list[index]['narration']
                                amount: int = data_list[index]['amount'] / 100
                                date: str = data_list[index]['date']
                                print(date)
                                if narration.find(AccountLinkage.objects.get(user=seller).fullName) and amount == transaction_instance.fiat_paid and this_day in date:
                                    print("found!")
                                    if asset == 'BTC':
                                        buyer_wallet = BitcoinWallet.objects.get(user=buyer)
                                        seller_wallet = BitcoinWallet.objects.get(user=seller)

                                        # send crypto to buyer and reduce frozen asset of seller
                                        seller_wallet.amount = str(round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        buyer_wallet.available = str(round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        print(buyer_wallet.available)
                                        seller_wallet.save()
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)
                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(escrow_instance.escrow_fee)
                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # record transactions on wallet for buyer and seller
                                        buyer_wallet_trx = WalletTransactionsHistory.objects.create(
                                            wallet=buyer_escrow_wallet,
                                            transaction_type='Debit',
                                            amount=float(escrow_instance.escrow_fee),
                                            transaction_key=random_string_generator(15),
                                            slug=random_string_generator()
                                        )

                                        seller_wallet_trx = WalletTransactionsHistory.objects.create(
                                            wallet=seller_escrow_wallet,
                                            transaction_type='Debit',
                                            amount=float(escrow_instance.escrow_fee),
                                            transaction_key=random_string_generator(15),
                                            slug=random_string_generator()
                                        )

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]
                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name, last_name=seller.last_name),
                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': request.user.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )

                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = seller

                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )

                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": timezone.now(),
                                                "success": bool(timezone.now())
                                            },

                                            status=status.HTTP_201_CREATED
                                        )
                                    elif asset == 'LTC':
                                        seller = P2PTransaction.objects.get(transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = LitecoinWallet.objects.get(user=buyer)
                                        seller_wallet = LitecoinWallet.objects.get(user=seller)

                                        # send crypto to buyer and reduce frozen asset of seller
                                        seller_wallet.amount = str(round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))

                                        buyer_wallet.available = str(
                                            round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))

                                        seller_wallet.save()
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(escrow_instance.escrow_fee)

                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # send email to seller notifying them that their trade has been sold
                                        context = {

                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=request.user.last_name),

                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone

                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]
                                        from django.core.mail import EmailMessage

                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )

                                        message.fail_silently = False
                                        message.send()

                                        # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name,
                                                                                        last_name=seller.last_name),
                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = seller

                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )

                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": timezone.now(),
                                                "success": bool(timezone.now())
                                            },
                                            status=status.HTTP_201_CREATED
                                        )

                                    elif asset == 'DOGE':
                                        seller = P2PTransaction.objects.get(transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = DogecoinWallet.objects.get(user=buyer)
                                        seller_wallet = DogecoinWallet.objects.get(user=seller)

                                        seller_wallet.amount = str(round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        buyer_wallet.available = str(round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        seller_wallet.save()
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(escrow_instance.escrow_fee)
                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name, last_name=seller.last_name),
                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )

                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = seller

                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )

                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": timezone.now(),
                                                "success": bool(timezone.now())
                                            },
                                            status=status.HTTP_201_CREATED
                                        )

                                    elif asset == 'ETH':
                                        seller = P2PTransaction.objects.get(transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = EthereumWallet.objects.get(user=buyer)
                                        seller_wallet = EthereumWallet.objects.get(user=seller)

                                        # transfer crypto to buyer
                                        receiver_address = buyer_wallet.public_key
                                        amount = data['cryptoUnits']
                                        gas_price = float(data['networkFee']) / 10

                                        decrypted_private_key = web3.eth.account.decrypt(
                                            keyfile_json=seller_wallet.encrypted_private_key,
                                            password=seller.username)
                                        nonce = web3.eth.getTransactionCount(seller_wallet.public_key)
                                        tx = {
                                            'nonce': nonce,
                                            'to': receiver_address,
                                            'value': web3.toWei(amount, 'ether'),
                                            'gas': 21000,
                                            'gasPrice': web3.toWei('{blockchain_gasFee}'.format(blockchain_gasFee=gas_price),'gwei')
                                        }

                                        signed_transaction = web3.eth.account.signTransaction(transaction_dict=tx, private_key=decrypted_private_key)
                                        tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

                                        seller_wallet.amount = str(round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        seller_wallet.previous_bal = str(round(float(seller_wallet.previous_bal) - float(data['cryptoUnits']), 8))
                                        seller_wallet.save()

                                        buyer_wallet.available = str(round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        buyer_wallet.previous_bal = str(round(float(buyer_wallet.previous_bal) + float(data['cryptoUnits']), 8))
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet
                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(escrow_instance.escrow_fee)
                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # notify buyer that the transaction was successful
                                        context = {

                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name,
                                                                                        last_name=seller.last_name),

                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = buyer

                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )

                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()

                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": web3.toHex(tx_hash),
                                                "success": bool(web3.toHex(tx_hash))
                                            },
                                            status=status.HTTP_201_CREATED
                                        )

                                    elif asset == 'USDT':
                                        seller = P2PTransaction.objects.get(transaction_key=data['transactionKey']).trade.trade_creator
                                        buyer_wallet = EthereumWallet.objects.get(user=buyer)
                                        seller_wallet = EthereumWallet.objects.get(user=seller)

                                        seller_wallet.amount = str(round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        buyer_wallet.available = str(round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        receiver_address = buyer_wallet.public_key

                                        amount = data['cryptoUnits']
                                        gas_price = float(request.data.get('networkFee', )) / 10

                                        tether_address = Web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
                                        tether_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"},{"name":"newMaxFee","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_blackListedUser","type":"address"}],"name":"destroyBlackFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_initialSupply","type":"uint256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Issue","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}]')

                                        tether_contract = web3.eth.contract(address=tether_address, abi=tether_abi)
                                        user_usdt_wallet = TetherUSDWallet.objects.get(user=seller)
                                        tether_user_address = Web3.toChecksumAddress(user_usdt_wallet.public_key)
                                        decrypted_private_key = web3.eth.account.decrypt(
                                            keyfile_json=user_usdt_wallet.encrypted_private_key,
                                            password=seller.username
                                        )

                                        nonce = web3.eth.getTransactionCount(tether_user_address)
                                        tx = tether_contract.functions.transfer(
                                            receiver_address,
                                            web3.toWei(amount, 'ether')).buildTransaction({
                                            'gas': 21000,
                                            'gasPrice': web3.toWei(
                                                '{blockchain_gasFee}'.format(blockchain_gasFee=gas_price), 'gwei'),
                                            'nonce': nonce
                                        })

                                        signed_tx = web3.eth.account.signTransaction(tx, private_key=decrypted_private_key)
                                        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

                                        seller_wallet.amount = str(round(float(seller_wallet.amount) - float(data['cryptoUnits']), 8))
                                        seller_wallet.previous_bal = str(round(float(seller_wallet.previous_bal) - float(data['cryptoUnits']), 8))
                                        seller_wallet.save()

                                        buyer_wallet.available = str(round(float(buyer_wallet.available) + float(data['cryptoUnits']), 8))
                                        buyer_wallet.previous_bal = str(round(float(buyer_wallet.previous_bal) + float(data['cryptoUnits']), 8))
                                        buyer_wallet.save()

                                        # subtract money from both buyer and seller fiat wallet

                                        buyer_escrow_wallet = FiatWallet.objects.get(user=buyer)
                                        seller_escrow_wallet = FiatWallet.objects.get(user=seller)

                                        buyer_escrow_wallet.balance = buyer_escrow_wallet.balance - float(escrow_instance.escrow_fee)
                                        seller_escrow_wallet.balance = seller_escrow_wallet.balance - float(escrow_instance.escrow_fee)

                                        buyer_escrow_wallet.save()
                                        seller_escrow_wallet.save()

                                        # send email to seller notifying them that their trade has been sold
                                        context = {
                                            'seller': seller.first_name,
                                            'buyer': "{first_name} {last_name}".format(
                                                first_name=buyer.first_name,
                                                last_name=buyer.last_name),

                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedSeller.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [seller.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # notify buyer that the transaction was successful
                                        context = {
                                            'seller': "{first_name} {last_name}".format(first_name=seller.first_name,
                                                                                        last_name=seller.last_name),
                                            'buyer': buyer.first_name,
                                            'tradeType': "SELL {asset}".format(asset=asset),
                                            'currency': data['currency'],
                                            'amount': amount,
                                            'narration': narration,
                                            'phone': buyer.profile.phone
                                        }

                                        html_ = get_template("p2p/emails/p2pTradeCompletedBuyer.html").render(context)
                                        subject = 'Vendescrow P2P Trade Completed'
                                        from_email = email_settings.EMAIL_HOST_USER
                                        recipient_list = [buyer.email]

                                        from django.core.mail import EmailMessage
                                        message = EmailMessage(
                                            subject, html_, from_email, recipient_list
                                        )
                                        message.fail_silently = False
                                        message.send()

                                        # set transaction status to completed
                                        trade_instance = P2PTrade.objects.get(slug=data['trade'])
                                        trade_customer = buyer
                                        transaction_instance = P2PTransaction.objects.get(
                                            transaction_key=data['transactionKey'],
                                            trade_visitor=trade_customer,
                                            trade=trade_instance
                                        )

                                        transaction_instance.status = "COMPLETED"
                                        transaction_instance.save()

                                        # activate the trade again
                                        trade_instance.active = True
                                        trade_instance.save()
                                        return Response(
                                            {
                                                'message': "transaction successful",
                                                "tx_": web3.toHex(tx_hash),
                                                "success": bool(web3.toHex(tx_hash))
                                            },
                                            status=status.HTTP_201_CREATED
                                        )
                                return Response(response, status=status_code)
                    return Response({"message": "Transaction not found"}, status=status_code)


class ModifyP2PTradeStatusAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        print(request.data)
        data = request.data
        instance = P2PTrade.objects.get(slug=data['trade'])
        instance.owner_cancel_trade = True
        instance.active = False
        instance.save()

        # move asset to back to user wallet
        asset = data.get('asset')
        if asset == 'BTC' and str(instance.trade_listed_as) == 'I WANT TO SELL':
            btc_instance = BitcoinWallet.objects.get(short_name=asset, user=instance.trade_creator)
            btc_instance.frozen = False
            btc_instance.available += btc_instance.amount
            btc_instance.save()
        elif asset == 'LTC' and str(instance.trade_listed_as) == 'I WANT TO SELL':
            ltc_instance = LitecoinWallet.objects.get(short_name=asset, user=instance.trade_creator)
            ltc_instance.frozen = False
            ltc_instance.available += ltc_instance.amount
            ltc_instance.save()
        elif asset == 'DOGE' and str(instance.trade_listed_as) == 'I WANT TO SELL':
            doge_instance = DogecoinWallet.objects.get(short_name=asset, user=instance.trade_creator)
            doge_instance.frozen = False
            doge_instance.available += doge_instance.amount
            doge_instance.save()
        elif asset == 'ETH' and str(instance.trade_listed_as) == 'I WANT TO SELL':
            eth_instance = EthereumWallet.objects.get(short_name=asset, user=instance.trade_creator)
            eth_instance.frozen = False
            eth_instance.available += eth_instance.amount
            eth_instance.save()
        elif asset == 'USDT' and str(instance.trade_listed_as) == 'I WANT TO SELL':
            usdt_instance = TetherUSDWallet.objects.get(short_name=asset, user=instance.trade_creator)
            usdt_instance.frozen = False
            usdt_instance.available += usdt_instance.amount
            usdt_instance.save()

        return Response({'message': 'Trade Cancelled Successfully'}, status=201)


class P2PTradeListPerUserAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = P2PTradeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 500

    def get_queryset(self):
        viewer_username = P2PTrade.objects.get(trade_creator=self.request.user, active=True)
        return P2PTrade.objects.filter(trade_creator__username=viewer_username)


class P2PTradeDetailPerUserAPIView(RetrieveAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = P2PTradeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 500

    def get_object(self):
        slug = self.kwargs["slug"]
        return get_object_or_404(P2PTrade, slug=slug)


class P2PTransactionListPerUser(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = P2PTransactionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 500

    def get_queryset(self):
        return P2PTransaction.objects.filter(trade_visitor=self.request.user)
