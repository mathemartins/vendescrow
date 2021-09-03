from django.contrib import admin


# Register your models here.
from notifications.models import NotificationURLS


class NotificationURLSModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'notification_id', 'timestamp', 'updated')
    list_display_links = ('user', 'notification_id',)
    search_fields = ('user',)


admin.site.register(NotificationURLS, NotificationURLSModelAdmin)
