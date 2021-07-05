from django.contrib import admin

# Register your models here.
from accounts.models import EmailActivation, Profile, UserLock, FavouriteAssets


class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'phone', 'keycode', 'ssn', 'country', 'country_flag', 'slug', 'timestamp', 'updated')
    list_display_links = ('user',)
    list_filter = ('user', 'phone')
    search_fields = ('user',)

    ordering = ('-timestamp',)
    fieldsets = (
        ('Basic Information', {'description': "Basic User Profile Information",
                               'fields': (('user',), 'keycode',)}),
        ('Complete Full Information',
         {'classes': ('collapse',), 'fields': ('phone', 'ssn', 'slug', 'country', 'country_flag')}),)


@admin.register(UserLock)
class UserLockModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'lock_key')
    list_display_links = ('user',)
    list_filter = ('user', 'lock_key')
    search_fields = ('user',)


@admin.register(FavouriteAssets)
class FavouriteAssetsModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'timestamp', 'updated')
    list_filter = ('slug', 'timestamp', 'updated')
    prepopulated_fields = {'slug': ('user',)}
    search_fields = ("user",)


admin.site.site_header = 'VendEscrow'
