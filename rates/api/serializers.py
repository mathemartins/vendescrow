from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from rates.models import FiatRate


class FiatRateListSerializer(ModelSerializer):
    country = SerializerMethodField()

    class Meta:
        model = FiatRate
        fields = [
            'country',
            'dollar_rate',
            'timestamp',
            'updated',
        ]

    def get_country(self, obj):
        print(obj)
        return str(obj)