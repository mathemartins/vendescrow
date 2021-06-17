from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class FiatWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.CharField(max_length=18, default=0, blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fiat_wallet"
        verbose_name = "Fiat Wallet"
        verbose_name_plural = "Fiat Wallets"

    def __str__(self):
        return self.balance
