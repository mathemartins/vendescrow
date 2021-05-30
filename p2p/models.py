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
        ('USDT', 'USDT'),
        ('DOGE', 'DOGE'),
        ('LITECOIN', 'LITECOIN'),
        ('DASH', 'DASH'),
        ('BITCOIN CASH', 'BITCOIN CASH'),
    )

    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_owner')
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_buyer', blank=True, null=True)
    trades = models.PositiveIntegerField(default=0)
    trade_listed_as = models.CharField(choices=TRADE_TYPE, max_length=20, default='SELL')
    vendor_rate_in_dollar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    crypto_trading_amount = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    min_trading_amount_in_fiat = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    max_trading_amount_in_fiat = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    asset_to_trade = models.CharField(choices=ASSET, max_length=20, default='BITCOIN')
    price_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=1.000, help_text="standard 1 dollar rate")
    min_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=0.980, help_text="minimum less than 1 dollar")
    max_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=1.020, help_text="maximum above 1 dollar")
    transaction_key = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.vendor.username)

