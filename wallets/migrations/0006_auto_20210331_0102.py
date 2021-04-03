# Generated by Django 3.1.7 on 2021-03-31 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0005_auto_20210330_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethereum_wallet',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=10, default=0, max_digits=999, null=True),
        ),
    ]
