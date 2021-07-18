from django.contrib import admin

# Register your models here.
from p2p.models import P2PTrade, P2PTransaction, P2PTradeCoreSettings


@admin.register(P2PTrade)
class P2PTradeModelAdmin(admin.ModelAdmin):
    list_display = ('trade_creator', 'transactions', 'trade_listed_as', 'creator_rate_in_dollar', 'asset_to_trade', 'timestamp', 'updated')
    list_editable = ('creator_rate_in_dollar', 'trade_listed_as')
    list_display_links = ('trade_creator', 'asset_to_trade')
    list_filter = ('trade_creator', 'transactions', 'trade_listed_as', 'timestamp', 'updated')
    search_fields = ('trade_creator', 'asset_to_trade', 'creator_rate_in_dollar')


@admin.register(P2PTransaction)
class P2PTransactionRegistration(admin.ModelAdmin):
    list_display = ('trade', 'transaction_key', 'trade_visitor', 'crypto_unit_transacted', 'status', 'fiat_paid')
    list_editable = ('status',)
    list_display_links = ('trade', 'transaction_key')
    list_filter = ('transaction_key', 'status')
    search_fields = ('transaction_key', 'trade_visitor', 'fiat_paid')


@admin.register(P2PTradeCoreSettings)
class P2PCoreSettings(admin.ModelAdmin):
    list_display = ('escrow_fee', 'timestamp', 'updated')
    list_editable = ('escrow_fee',)
