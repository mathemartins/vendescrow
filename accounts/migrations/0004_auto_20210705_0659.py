# Generated by Django 3.1.7 on 2021-07-05 13:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20210705_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='favouriteassets',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='favouriteassets',
            unique_together={('user', 'slug')},
        ),
    ]
