import json

from django.db.models import Q
from django.template.loader import get_template
from rest_framework import mixins, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from p2p.api.serializers import P2PTradeSerializer
from p2p.models import P2PTrade, P2PTradeCoreSettings, P2PTransaction
from vendescrow import email_settings
from vendescrow.utils import round_decimals_down, unique_id_generator


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
                active=True).filter(trade_listed_as="I WANT TO SELL").exclude(
                trade_creator__username=viewer_username).order_by('?')
        except P2PTrade.DoesNotExist:
            return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
                active=True).filter(trade_listed_as="I WANT TO SELL").order_by('?')


class ListBuyP2PAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication, JSONWebTokenAuthentication]
    serializer_class = P2PTradeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    paginate_by = 500

    def get_queryset(self):
        try:
            viewer_username = P2PTrade.objects.get(trade_creator=self.request.user, active=True)
            return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
                active=True).filter(trade_listed_as="I WANT TO BUY").exclude(
                trade_creator__username=viewer_username).order_by('?')
        except P2PTrade.DoesNotExist:
            return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
                active=True).filter(trade_listed_as="I WANT TO BUY").order_by('?')


class DetailP2PAPIView(RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    serializer_class = P2PTradeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        viewer_username = P2PTrade.objects.get(trade_creator=self.request.user, active=True).trade_creator.username
        return P2PTrade.objects.filter(trade_creator__profile__country=self.request.user.profile.country).filter(
            active=True).exclude(trade_creator__username=viewer_username)

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


class P2PTradeTransactionRetrieveAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, *args, **kwargs):
        print(kwargs)
        trade_instance = P2PTrade.objects.get(slug=kwargs.get('slug'))
        transaction_key = kwargs.get('transaction_key')
        user_transaction_instance = P2PTransaction.objects.get(trade=trade_instance, trade_visitor=request.user, transaction_key=transaction_key)
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
                'status': user_transaction_instance.status,
                'slug': user_transaction_instance.transaction_key,
            }]
        }
        return Response(response, status=status_code)


class P2PTradeTransactionAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def post(self, request, *args, **kwargs):
        data = request.data
        ACTION_CANCELLED = 0
        ACTION_CREATE = 1
        ACTION_APPEAL = 2
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
                'seller_account_numer': trade_instance.trade_creator.accountlinkage.account_number,
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
                             'tradeNarration': '{narration}'.format(narration=trade_identifier)}, status=201)

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

            return Response({'message': 'Trade Transaction Cancelled Successfully'}, status=201)
        elif data['actionType'] == ACTION_APPEAL:
            trade_instance = P2PTrade.objects.get(slug=data['trade'])
            trade_customer = request.user
            transaction_instance = P2PTransaction.objects.get(transaction_key=data['transactionKey'],
                                                              trade_visitor=trade_customer, trade=trade_instance)
            transaction_instance.status = "ON_APPEAL"
            transaction_instance.save()

            # activate the trade again
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

            return Response({'message': 'Trade Transaction Has Been Placed On Appeal Successfully'}, status=201)
