from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    sender = models.CharField(max_length=299, blank=True, null=True)
    receiver = models.CharField(max_length=299, blank=True, null=True)
    amount = models.CharField(max_length=299, blank=True, null=True)
    transaction_hash = models.CharField(max_length=299, blank=True, null=True)
    asset_type = models.CharField(max_length=299, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.transaction_hash)

    class Meta:
        ordering = ['timestamp']
