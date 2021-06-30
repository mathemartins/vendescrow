# Generated by Django 3.1.7 on 2021-06-30 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coincmc',
            name='circulating_supply',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coincmc',
            name='date_added',
            field=models.DateField(max_length=50),
        ),
        migrations.AlterField(
            model_name='coincmc',
            name='last_updated',
            field=models.DateField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coincmc',
            name='max_supply',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coincmc',
            name='number_of_market_pairs',
            field=models.FloatField(max_length=50),
        ),
        migrations.AlterField(
            model_name='coincmc',
            name='platform',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coincmc',
            name='total_supply',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='last_updated',
            field=models.DateField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='market_cap',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='percent_change1h',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='percent_change24h',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='percent_change30d',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='percent_change60d',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='percent_change7d',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='percent_change90d',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usd',
            name='price',
            field=models.FloatField(max_length=50),
        ),
        migrations.AlterField(
            model_name='usd',
            name='volume_24h',
            field=models.FloatField(blank=True, max_length=50, null=True),
        ),
    ]
