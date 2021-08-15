# Generated by Django 3.2.5 on 2021-08-15 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_alter_address_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1, verbose_name="Type d'adresse"),
        ),
    ]
