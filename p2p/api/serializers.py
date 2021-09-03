from rest_framework import serializers

from p2p.models import P2PTrade, P2PTransaction


class P2PTradeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField('api-p2p:detail', lookup_field='slug')
    trade_creator_username = serializers.SerializerMethodField('get_trade_creator')

    class Meta:
        model = P2PTrade
        fields = [
            'url',
            'id',
            'trade_creator',
            'trade_creator_username',
            'transactions',
            'trade_listed_as',
            'creator_rate_in_dollar',
            'crypto_trading_amount',
            'min_trading_amount_in_fiat',
            'max_trading_amount_in_fiat',
            'asset_to_trade',
            'price_slippage',
            'min_slippage',
            'max_slippage',
            'active',
            'slug',
            'timestamp',
            'updated',
        ]

    def get_trade_creator(self, obj):  # where obj is instance of the model class
        return obj.trade_creator.username


class P2PTransactionSerializer(serializers.ModelSerializer):
    trade_slug = serializers.SerializerMethodField('get_trade_slug')
    trade_creator_username = serializers.SerializerMethodField('get_trade_creator')
    trade_visitor_username = serializers.SerializerMethodField('get_trade_visitor')

    class Meta:
        model = P2PTransaction
        fields = [
            'id',
            'trade',
            'trade_slug',
            'transaction_key',
            'trade_creator_username',
            'trade_visitor_username',
            'crypto_unit_transacted',
            'fiat_paid',
            'status',
            'slug',
            'timestamp',
            'updated',
        ]

    def get_trade_slug(self, obj: P2PTransaction):  # where obj is instance of the model class
        return obj.slug

    def get_trade_creator(self, obj: P2PTransaction):  # where obj is instance of the model class
        return obj.trade.trade_creator.username

    def get_trade_visitor(self, obj: P2PTransaction):  # where obj is instance of the model class
        return obj.trade_visitor.username