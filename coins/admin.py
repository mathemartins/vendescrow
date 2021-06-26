from django.contrib import admin

# Register your models here.
from coins.models import CoinCMC, USD, Quote, CoinGecko

admin.site.register(CoinCMC)
admin.site.register(USD)
admin.site.register(Quote)
admin.site.register(CoinGecko)
