from django.contrib import admin


# Register your models here.
from mono.models import AccountLinkage


@admin.register(AccountLinkage)
class AccountLinkageAdmin(admin.ModelAdmin):
    list_display = ('user', 'mono_code', 'exchange_token', 'bvn', 'account_number', 'timestamp', 'updated')
    list_display_links = ('user', 'mono_code', 'exchange_token')
    search_fields = ('user', 'bvn', 'account_number')
    list_filter = ('user', 'account_number')