# Generated by Django 3.2.5 on 2021-08-12 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('amount', models.FloatField(verbose_name='Montant')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'expiration")),
                ('is_active', models.BooleanField(default=False, verbose_name='Actif')),
            ],
        ),
    ]