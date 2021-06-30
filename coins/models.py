from django.db import models


# Create your models here.

class CoinCMC(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    number_of_market_pairs = models.FloatField(max_length=50)
    date_added = models.DateField(max_length=50)
    max_supply = models.CharField(max_length=50, blank=True, null=True)
    circulating_supply = models.CharField(max_length=50, blank=True, null=True)
    total_supply = models.CharField(max_length=50, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)
    cmc_rank = models.IntegerField(default=0)
    last_updated = models.DateField(max_length=50, blank=True, null=True)
    quote = models.OneToOneField(to='coins.Quote', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.symbol


class Quote(models.Model):
    usd = models.OneToOneField(to='coins.USD', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.usd.price)


class USD(models.Model):
    price = models.FloatField(max_length=50)
    volume_24h = models.FloatField(max_length=50, blank=True, null=True)
    percent_change1h = models.FloatField(max_length=50, blank=True, null=True)
    percent_change24h = models.FloatField(max_length=50, blank=True, null=True)
    percent_change7d = models.FloatField(max_length=50, blank=True, null=True)
    percent_change30d = models.FloatField(max_length=50, blank=True, null=True)
    percent_change60d = models.FloatField(max_length=50, blank=True, null=True)
    percent_change90d = models.FloatField(max_length=50, blank=True, null=True)
    market_cap = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateField(max_length=50, blank=True, null=True)

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
