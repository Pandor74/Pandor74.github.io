# Generated by Django 2.0.6 on 2018-09-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborateurs', '0014_auto_20180920_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='projet',
            name='agence',
            field=models.CharField(blank=True, choices=[('Annecy', 'Annecy'), ('Lyon', 'Lyon')], default='Annecy', max_length=20, null=True, verbose_name='Agence interne'),
        ),
    ]
