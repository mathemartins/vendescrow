from rest_framework import serializers

from p2p.models import P2PTrade


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

    def get_trade_creator(self, obj): # where obj is instance of the model class
        return obj.trade_creator.username

