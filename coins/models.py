from django.db import models


# Create your models here.

class CoinCMC(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    number_of_market_pairs = models.CharField(max_length=50)
    date_added = models.CharField(max_length=50)
    max_supply = models.CharField(max_length=50)
    circulating_supply = models.CharField(max_length=50)
    total_supply = models.CharField(max_length=50)
    platform = models.CharField(max_length=50)
    cmc_rank = models.IntegerField(default=0)
    last_updated = models.CharField(max_length=50)
    quote = models.OneToOneField(to='coins.Quote', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.symbol


class Quote(models.Model):
    usd = models.OneToOneField(to='coins.USD', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.usd.price)


class USD(models.Model):
    price = models.CharField(max_length=50)
    volume_24h = models.CharField(max_length=50)
    percent_change1h = models.CharField(max_length=50)
    percent_change24h = models.CharField(max_length=50)
    percent_change7d = models.CharField(max_length=50)
    percent_change30d = models.CharField(max_length=50)
    percent_change60d = models.CharField(max_length=50)
    percent_change90d = models.CharField(max_length=50)
    market_cap = models.CharField(max_length=50)
    last_updated = models.CharField(max_length=50)

    def __str__(self):
        return self.price


class CoinGecko(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    price = models.FloatField(default=0, blank=True, null=True)
    rank = models.IntegerField(default=0, blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.name)
