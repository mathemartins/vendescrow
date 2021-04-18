# Generated by Django 3.1.7 on 2021-04-18 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PeerToPeerTrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trades', models.PositiveIntegerField(default=0)),
                ('trade_listed_as', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], default='SELL', max_length=20)),
                ('vendor_rate_in_dollar', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('crypto_amount', models.DecimalField(decimal_places=18, max_digits=20)),
                ('asset_to_trade', models.CharField(choices=[('ETHEREUM', 'ETHEREUM'), ('BITCOIN', 'BITCOIN'), ('LITECOIN', 'LITECOIN')], default='BITCOIN', max_length=20)),
                ('transaction_key', models.CharField(blank=True, max_length=20, null=True)),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_purchaser', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
