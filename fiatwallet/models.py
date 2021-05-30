from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class FiatWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=11, blank=True, null=True)
    account_name = models.CharField(max_length=256, blank=True, null=True)
    bank = models.CharField(max_length=256, blank=True, null=True)
    balance = models.CharField(max_length=18, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fiat_wallet"
        verbose_name = "Fiat Wallet"
        verbose_name_plural = "Fiat Wallets"

    def __str__(self):
        return self.account_name
