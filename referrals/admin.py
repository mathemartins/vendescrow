from django.contrib import admin

# Register your models here.
from referrals.models import EarlyBirdAccess


@admin.register(EarlyBirdAccess)
class EarlyBirdAccessModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'referral_code', 'number_of_referrals', 'base_url', 'timestamp')
    list_filter = ('number_of_referrals',)
    search_fields = ("email", "referral_code")
