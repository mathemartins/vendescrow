from rest_framework import serializers

from fiatwallet.models import FiatWallet


class EscrowWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiatWallet
        fields = [
            'user',
            'balance',
            'active',
            'slug',
            'timestamp',
            'updated',
        ]

