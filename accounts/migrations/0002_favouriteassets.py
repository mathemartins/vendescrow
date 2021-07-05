# Generated by Django 3.1.7 on 2021-07-05 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coins', '0008_coin_price_change_in_the_last_1hr'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteAssets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('favourite_coins', models.ManyToManyField(to='coins.Coin')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Favourite Asset',
                'verbose_name_plural': 'Favourite Assets',
                'db_table': 'favourite_assets',
                'unique_together': {('user', 'slug')},
            },
        ),
    ]