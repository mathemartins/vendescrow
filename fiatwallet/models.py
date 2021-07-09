from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from vendescrow.utils import random_string_generator


class FiatWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(max_length=18, default=0, blank=True, null=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fiat_wallet"
        verbose_name = "Escrow Wallet"
        verbose_name_plural = "Escrow Wallets"

    def __str__(self):
        return str(self.balance)


class WalletTransactionsHistory(models.Model):
    WALLET_TRANSACTION_TYPE = (
        ('Wallet Created', 'Wallet Created'),
        ('Credit', 'Credit'),
        ('Debit', 'Debit')
    )
    wallet = models.ForeignKey(to='fiatwallet.FiatWallet', on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=WALLET_TRANSACTION_TYPE, max_length=300, default='Credit')
    amount = models.FloatField(max_length=18, default=0, blank=True, null=True)
    transaction_key = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "wallet_tranactions"
        verbose_name = "Escrow Wallet Transaction"
        verbose_name_plural = "Escrow Wallet Transactions"

    def __str__(self):
        return str(self.transaction_key)


@receiver(post_save, sender=FiatWallet)
def fiat_wallet_transaction_presave_receiver(sender, instance, created, *args, **kwargs):
    if created:
        WalletTransactionsHistory.objects.create(
            wallet=instance,
            transaction_type='Wallet Created',
            amount=0.0,
            transaction_key=random_string_generator(15),
            slug=random_string_generator()
        )
