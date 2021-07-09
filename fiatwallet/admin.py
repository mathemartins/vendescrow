from django.contrib import admin

# Register your models here.
from fiatwallet.models import FiatWallet, WalletTransactionsHistory


@admin.register(FiatWallet)
class FiatWalletModelAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "active", "timestamp",)
    list_filter = ("user", "active", "slug",)
    search_fields = ("user", "balance",)
    prepopulated_fields = {"slug": ["user"]}


admin.site.register(WalletTransactionsHistory)
