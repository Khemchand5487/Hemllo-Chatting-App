# Generated by Django 3.1.7 on 2021-04-18 08:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210320_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
