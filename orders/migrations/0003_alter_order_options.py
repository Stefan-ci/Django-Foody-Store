# Generated by Django 3.2.5 on 2021-08-12 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Commande', 'verbose_name_plural': 'Commandes'},
        ),
    ]
