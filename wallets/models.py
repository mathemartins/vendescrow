from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# class BitcoinWallet(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     short_name = models.CharField(max_length=12, default='BTC')
#     icon = models.URLField(blank=True, null=True)
#     private_key = models.CharField(max_length=256)
#     public_key = models.CharField(max_length=256)
#     pass


class Ethereum_Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='Ethereum')
    short_name = models.CharField(max_length=12, default='ETH')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=999, decimal_places=10, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ethereum_wallet"
        verbose_name = "Ethereum Wallet"
        verbose_name_plural = "Ethereum Wallets"

    def __str__(self):
        return self.public_key


# class LitecoinWallet(models.Model):
#     pass
#
#
# class Dodgecoin(models.Model):
#     pass
#
#
# class BitcoinCashWallet(models.Model):
#     pass
#
#
# class Ripple(models.Model):
#     pass
#
#
# class TronWallet(models.Model):
#     pass
#
#
# class KleverWallet(models.Model):
#     pass
#
#
# class VendWallet(models.Model):
#     pass
