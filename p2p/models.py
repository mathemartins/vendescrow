from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class PeerToPeerTrade(models.Model):
    TRADE_TYPE = (
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    )

    ASSET = (
        ('ETHEREUM', 'ETHEREUM'),
        ('BITCOIN', 'BITCOIN'),
        ('LITECOIN', 'LITECOIN'),
    )

    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_owner')
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_purchaser')
    trades = models.PositiveIntegerField(default=0)
    trade_listed_as = models.CharField(choices=TRADE_TYPE, max_length=20, default='SELL')
    vendor_rate_in_dollar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    crypto_amount = models.DecimalField(max_digits=20, decimal_places=18)
    asset_to_trade = models.CharField(choices=ASSET, max_length=20, default='BITCOIN')
    transaction_key = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.vendor.username)

