# Generated by Django 3.1.7 on 2021-06-30 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0003_auto_20210630_0317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coin',
            name='price_change_percentage_1h_in_usd',
        ),
    ]