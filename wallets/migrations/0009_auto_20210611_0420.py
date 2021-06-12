# Generated by Django 3.1.7 on 2021-06-11 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0008_delete_bitcoincashwallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitcoinwallet',
            name='short_nameBTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='bitcoinwallet',
            name='short_nameDOGE',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='bitcoinwallet',
            name='short_nameLTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='dashwallet',
            name='short_nameBTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='dashwallet',
            name='short_nameDOGE',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='dashwallet',
            name='short_nameLTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='dogecoinwallet',
            name='short_nameBTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='dogecoinwallet',
            name='short_nameDOGE',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='dogecoinwallet',
            name='short_nameLTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='ethereumwallet',
            name='short_nameBTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='ethereumwallet',
            name='short_nameDOGE',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='ethereumwallet',
            name='short_nameLTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='litecoinwallet',
            name='short_nameBTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='litecoinwallet',
            name='short_nameDOGE',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='litecoinwallet',
            name='short_nameLTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='tetherusdwallet',
            name='short_nameBTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='tetherusdwallet',
            name='short_nameDOGE',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='tetherusdwallet',
            name='short_nameLTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='vendtokenwallet',
            name='short_nameBTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='vendtokenwallet',
            name='short_nameDOGE',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='vendtokenwallet',
            name='short_nameLTC',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]