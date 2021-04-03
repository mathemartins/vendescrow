from django.contrib import admin

from rates.models import FiatRate


# Register your models here.

class FiatRateModelAdmin(admin.ModelAdmin):
    list_display = ["country", "dollar_rate", "timestamp", "updated"]
    list_display_links = ["country", "updated"]
    list_editable = ["dollar_rate"]
    list_filter = ["updated", "timestamp"]

    search_fields = ["country",]

    class Meta:
        model = FiatRate


admin.site.register(FiatRate, FiatRateModelAdmin)
