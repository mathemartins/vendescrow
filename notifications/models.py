from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class NotificationURLS(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True) # Sample url - https://api.vendescrow.com/notify/username
    notification_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification_url"
        verbose_name = "Notification URLS"
        verbose_name_plural = "Notification URLS"

    def __str__(self):
        return self.user.email
