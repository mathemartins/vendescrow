from django.contrib import admin

from wallets.models import EthereumWallet, TetherUSDWallet, VendTokenWallet, BitcoinWallet


# Register your models here.

@admin.register(BitcoinWallet)
class BitcoinWalletModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_name', 'icon', 'private_key', 'public_key', 'address', 'timestamp', 'updated')
    list_editable = ('icon', 'short_name')
    list_display_links = ('user', 'public_key')
    list_filter = ('user', 'timestamp', 'updated')
    search_fields = ('user', 'public_key')


@admin.register(EthereumWallet)
class EthereumWalletModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_name', 'icon', 'encrypted_private_key', 'public_key', 'timestamp', 'updated')
    list_editable = ('icon', 'short_name')
    list_display_links = ('user', 'public_key')
    list_filter = ('user', 'timestamp', 'updated')
    search_fields = ('user', 'public_key')


@admin.register(TetherUSDWallet)
class TetherUSDWalletModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_name', 'icon', 'encrypted_private_key', 'public_key', 'timestamp', 'updated')
    list_editable = ('icon', 'short_name')
    list_display_links = ('user', 'public_key')
    list_filter = ('user', 'timestamp', 'updated')
    search_fields = ('user', 'public_key')


@admin.register(VendTokenWallet)
class VendTokenWalletModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_name', 'icon', 'encrypted_private_key', 'public_key', 'timestamp', 'updated')
    list_editable = ('icon', 'short_name')
    list_display_links = ('user', 'public_key')
    list_filter = ('user', 'timestamp', 'updated')
    search_fields = ('user', 'public_key')
