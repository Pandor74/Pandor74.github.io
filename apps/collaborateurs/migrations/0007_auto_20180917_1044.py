# Generated by Django 2.0.6 on 2018-09-17 08:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborateurs', '0006_auto_20180914_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='date_exe',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Date de démarrage des travaux (facultatif) '),
        ),
    ]
