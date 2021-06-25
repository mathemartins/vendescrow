from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from rates.models import FiatRate
from vendescrow.utils import unique_slug_generator, round_decimals_down
from wallets.models import BitcoinWallet, LitecoinWallet, DogecoinWallet, EthereumWallet, TetherUSDWallet


class P2PTrade(models.Model):
    TRADE_TYPE = (
        ('I WANT TO BUY', 'I WANT TO BUY'),
        ('I WANT TO SELL', 'I WANT TO SELL'),
    )

    ASSET = (
        ('ETH', 'ETH'),
        ('BTC', 'BTC'),
        ('USDT', 'USDT'),
        ('DOGE', 'DOGE'),
        ('LTC', 'LTC'),
    )

    trade_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_author')
    transactions = models.PositiveIntegerField(default=0)
    trade_listed_as = models.CharField(choices=TRADE_TYPE, max_length=20, default='I WANT TO SELL')
    creator_rate_in_dollar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    crypto_trading_amount = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    min_trading_amount_in_fiat = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    max_trading_amount_in_fiat = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    asset_to_trade = models.CharField(choices=ASSET, max_length=20, default='BTC')
    price_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=1.000,
                                         help_text="standard 1 dollar rate")
    min_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=0.980,
                                       help_text="minimum less than 1 dollar")
    max_slippage = models.DecimalField(max_digits=4, decimal_places=3, default=1.020,
                                       help_text="maximum above 1 dollar")
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "p2p"
        verbose_name = "P2P Trade"
        verbose_name_plural = "P2P Trades"

    def __str__(self):
        return str(self.trade_creator)

    def get_absolute_url(self):
        if self.active:
            return reverse("p2p:trades", kwargs={"slug": self.slug})


@receiver(pre_save, sender=P2PTrade)
def my_callback(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = unique_slug_generator(instance)

    black_market_rate = FiatRate.objects.get(country=instance.trade_creator.profile.country).dollar_rate

    if instance.creator_rate_in_dollar is None:
        instance.creator_rate_in_dollar = round_decimals_down((float(instance.price_slippage) * float(black_market_rate)))

    asset = str(instance.asset_to_trade)
    if asset == 'BTC' and str(instance.trade_listed_as) == 'I WANT TO SELL':
        btc_instance = BitcoinWallet.objects.get(short_name=asset, user=instance.trade_creator)
        if float(btc_instance.available) > float(instance.crypto_trading_amount):
            btc_instance.available = round_decimals_down((float(btc_instance.available) - float(instance.crypto_trading_amount)))
            btc_instance.frozen = True
            btc_instance.amount = instance.crypto_trading_amount
            btc_instance.save()
    elif asset == 'LTC' and str(instance.trade_listed_as) == 'I WANT TO SELL':
        ltc_instance = LitecoinWallet.objects.get(short_name=asset, user=instance.trade_creator)
        if float(ltc_instance.available) > float(instance.crypto_trading_amount):
            ltc_instance.available = round_decimals_down((float(ltc_instance.available) - float(instance.crypto_trading_amount)))
            ltc_instance.frozen = True
            ltc_instance.amount = instance.crypto_trading_amount
            ltc_instance.save()
    elif asset == 'DOGE' and str(instance.trade_listed_as) == 'I WANT TO SELL':
        doge_instance = DogecoinWallet.objects.get(short_name=asset, user=instance.trade_creator)
        if float(doge_instance.available) > float(instance.crypto_trading_amount):
            doge_instance.available = round_decimals_down((float(doge_instance.available) - float(instance.crypto_trading_amount)))
            doge_instance.frozen = True
            doge_instance.amount = instance.crypto_trading_amount
            doge_instance.save()
    elif asset == 'ETH' and str(instance.trade_listed_as) == 'I WANT TO SELL':
        eth_instance = EthereumWallet.objects.get(short_name=asset, user=instance.trade_creator)
        if float(eth_instance.available) > float(instance.crypto_trading_amount):
            eth_instance.available = round_decimals_down((float(eth_instance.available) - float(instance.crypto_trading_amount)))
            eth_instance.frozen = True
            eth_instance.amount = instance.crypto_trading_amount
            eth_instance.save()
    elif asset == 'USDT' and str(instance.trade_listed_as) == 'I WANT TO SELL':
        usdt_instance = TetherUSDWallet.objects.get(short_name=asset, user=instance.trade_creator)
        if float(usdt_instance.available) > float(instance.crypto_trading_amount):
            usdt_instance.available = round_decimals_down((float(usdt_instance.available) - float(instance.crypto_trading_amount)))
            usdt_instance.frozen = True
            usdt_instance.amount = instance.crypto_trading_amount
            usdt_instance.save()


class P2PTransaction(models.Model):
    TRANSACTION_STATUS = (
        ('RUNNING', 'RUNNING'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELLED', 'CANCELLED'),
        ('ON_APPEAL', 'ON_APPEAL'),
    )

    trade = models.ForeignKey(P2PTrade, on_delete=models.CASCADE)
    transaction_key = models.CharField(max_length=300, blank=True, null=True)
    trade_visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_viewer')
    crypto_unit_transacted = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    fiat_paid = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=20, default='RUNNING')
    slug = models.SlugField(max_length=300, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "p2p_transaction"
        verbose_name = "P2P Trade Transactions"
        verbose_name_plural = "P2P Trade Transactions"

    def __str__(self):
        return str(self.trade_creator)

    def get_absolute_url(self):
        if self.active:
            return reverse("p2p:trades", kwargs={"slug": self.slug})
