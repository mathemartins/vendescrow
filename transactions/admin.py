from django.contrib import admin

# Register your models here.
from transactions.models import Transaction


@admin.register(Transaction)
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount', 'asset_type', 'transaction_hash', 'timestamp')
    list_display_links = ('sender', 'amount', 'transaction_hash')
    search_fields = ('sender', 'receiver', 'transaction_hash')
    list_filter = ('sender', 'receiver', 'amount', 'asset_type', 'transaction_hash')
