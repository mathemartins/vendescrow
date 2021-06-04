# Generated by Django 3.1.7 on 2021-05-29 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('p2p', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='peertopeertrade',
            name='max_slippage',
            field=models.DecimalField(decimal_places=3, default=1.02, help_text='maximum above 1 dollar', max_digits=4),
        ),
        migrations.AddField(
            model_name='peertopeertrade',
            name='min_slippage',
            field=models.DecimalField(decimal_places=3, default=0.98, help_text='minimum less than 1 dollar', max_digits=4),
        ),
        migrations.AddField(
            model_name='peertopeertrade',
            name='price_slippage',
            field=models.DecimalField(decimal_places=3, default=1.0, help_text='standard 1 dollar rate', max_digits=4),
        ),
        migrations.AlterField(
            model_name='peertopeertrade',
            name='asset_to_trade',
            field=models.CharField(choices=[('ETHEREUM', 'ETHEREUM'), ('BITCOIN', 'BITCOIN'), ('USDT', 'USDT'), ('DOGE', 'DOGE'), ('LITECOIN', 'LITECOIN')], default='BITCOIN', max_length=20),
        ),
        migrations.AlterField(
            model_name='peertopeertrade',
            name='purchaser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset_buyer', to=settings.AUTH_USER_MODEL),
        ),
    ]