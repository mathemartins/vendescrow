# Generated by Django 3.1.7 on 2021-05-03 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethereumwallet',
            name='amount',
            field=models.CharField(blank=True, default=0, max_length=18, null=True),
        ),
    ]
