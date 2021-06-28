# Generated by Django 3.1.7 on 2021-06-28 15:59

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
            name='AccountLinkage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(blank=True, max_length=299, null=True)),
                ('mono_code', models.CharField(blank=True, max_length=299, null=True)),
                ('exchange_token', models.CharField(blank=True, max_length=299, null=True)),
                ('email', models.CharField(blank=True, max_length=300, null=True)),
                ('phone', models.CharField(blank=True, max_length=300, null=True)),
                ('gender', models.CharField(blank=True, max_length=300, null=True)),
                ('bvn', models.CharField(blank=True, max_length=300, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=300, null=True)),
                ('home_address', models.CharField(blank=True, max_length=300, null=True)),
                ('office_address', models.CharField(blank=True, max_length=300, null=True)),
                ('bank', models.CharField(blank=True, max_length=300, null=True)),
                ('account_number', models.CharField(blank=True, max_length=300, null=True)),
                ('account_type', models.CharField(blank=True, max_length=300, null=True)),
                ('currency', models.CharField(blank=True, max_length=300, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account Linkage',
                'verbose_name_plural': 'Accounts Linkage',
                'db_table': 'account_linkage',
            },
        ),
    ]
