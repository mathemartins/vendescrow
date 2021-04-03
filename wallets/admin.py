from django.contrib import admin

from wallets.models import Ethereum_Wallet


# Register your models here.

@admin.register(Ethereum_Wallet)
class EthereumWalletModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_name', 'icon', 'encrypted_private_key', 'public_key', 'timestamp', 'updated')
    list_editable = ('icon', 'short_name')
    list_display_links = ('user', 'public_key')
    list_filter = ('user', 'timestamp', 'updated')
    search_fields = ('user', 'public_key')
