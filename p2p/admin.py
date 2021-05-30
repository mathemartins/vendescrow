from django.contrib import admin

# Register your models here.
from p2p.models import PeerToPeerTrade


@admin.register(PeerToPeerTrade)
class PeerToPeerTradeModelAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'purchaser', 'trades', 'trade_listed_as', 'vendor_rate_in_dollar', 'transaction_key', 'timestamp', 'updated')
    list_editable = ('trades', 'trade_listed_as')
    list_display_links = ('vendor', 'purchaser')
    list_filter = ('vendor', 'purchaser', 'trade_listed_as', 'transaction_key', 'timestamp', 'updated')
    search_fields = ('vendor', 'purchaser', 'transaction_key')