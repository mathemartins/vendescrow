from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class BitcoinWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='Bitcoin')
    short_name = models.CharField(max_length=12, default='BTC')
    icon = models.URLField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    wif = models.CharField(max_length=256, blank=True, null=True)
    previous_bal = models.CharField(max_length=18, default=0, blank=True, null=True)
    available = models.CharField(max_length=18, default=0, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    amount = models.CharField(max_length=18, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bitcoin_wallet"
        verbose_name = "Bitcoin Wallet"
        verbose_name_plural = "Bitcoin Wallets"

    def __str__(self):
        return self.address


class DogecoinWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='Dogecoin')
    short_name = models.CharField(max_length=12, default='DOGE')
    icon = models.URLField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    wif = models.CharField(max_length=256, blank=True, null=True)
    previous_bal = models.CharField(max_length=18, default=0, blank=True, null=True)
    available = models.CharField(max_length=18, default=0, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    amount = models.CharField(max_length=18, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dogecoin_wallet"
        verbose_name = "Dogecoin Wallet"
        verbose_name_plural = "Dogecoin Wallets"

    def __str__(self):
        return self.address


class LitecoinWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='Litecoin')
    short_name = models.CharField(max_length=12, default='LTC')
    icon = models.URLField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    wif = models.CharField(max_length=256, blank=True, null=True)
    previous_bal = models.CharField(max_length=18, default=0, blank=True, null=True)
    available = models.CharField(max_length=18, default=0, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    amount = models.CharField(max_length=18, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "litecoin_wallet"
        verbose_name = "Litecoin Wallet"
        verbose_name_plural = "Litecoin Wallets"

    def __str__(self):
        return self.address


class DashWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='Dash')
    short_name = models.CharField(max_length=12, default='DASH')
    icon = models.URLField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    wif = models.CharField(max_length=256, blank=True, null=True)
    previous_bal = models.CharField(max_length=18, default=0, blank=True, null=True)
    available = models.CharField(max_length=18, default=0, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    amount = models.CharField(max_length=18, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Dash_wallet"
        verbose_name = "Dash Wallet"
        verbose_name_plural = "Dash Wallets"

    def __str__(self):
        return self.address


class EthereumWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='Ethereum')
    short_name = models.CharField(max_length=12, default='ETH')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True)
    previous_bal = models.CharField(max_length=18, default=0, blank=True, null=True)
    available = models.CharField(max_length=18, default=0, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    amount = models.CharField(max_length=18, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ethereum_wallet"
        verbose_name = "Ethereum Wallet"
        verbose_name_plural = "Ethereum Wallets"

    def __str__(self):
        return self.public_key


class TetherUSDWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='Tether USD')
    short_name = models.CharField(max_length=12, default='USDT')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True)
    previous_bal = models.CharField(max_length=18, default=0, blank=True, null=True)
    available = models.CharField(max_length=18, default=0, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    amount = models.CharField(max_length=18, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tetherusd_wallet"
        verbose_name = "TetherUSD Wallet"
        verbose_name_plural = "TetherUSD Wallets"

    def __str__(self):
        return self.public_key


class VendTokenWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default='VendToken')
    short_name = models.CharField(max_length=12, default='VDT')
    icon = models.URLField(blank=True, null=True)
    encrypted_private_key = models.TextField(blank=True, null=True)
    public_key = models.CharField(max_length=256, blank=True, null=True)
    previous_bal = models.CharField(max_length=18, default=0, blank=True, null=True)
    available = models.CharField(max_length=18, default=0, blank=True, null=True)
    frozen = models.BooleanField(default=False)
    amount = models.CharField(max_length=18, default=0, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vendtoken_wallet"
        verbose_name = "VendToken Wallet"
        verbose_name_plural = "VendToken Wallets"

    def __str__(self):
        return self.public_key
