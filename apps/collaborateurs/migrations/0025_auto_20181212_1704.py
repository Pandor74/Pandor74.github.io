# Generated by Django 2.1.2 on 2018-12-12 17:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collaborateurs', '0024_auto_20181212_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personne',
            name='date_inscription_personne',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 12, 17, 4, 10, 154926, tzinfo=utc), verbose_name="Date d'inscription "),
        ),
    ]