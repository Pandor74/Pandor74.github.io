# Generated by Django 2.1.2 on 2018-12-14 14:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collaborateurs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personne',
            name='date_inscription_personne',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 14, 14, 29, 21, 491127, tzinfo=utc), verbose_name="Date d'inscription "),
        ),
    ]