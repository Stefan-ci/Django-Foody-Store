# Generated by Django 3.2.5 on 2021-08-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_item_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('steak', 'Steak'), ('vegan', 'Vegan'), ('vegetarian', 'Vegetarian'), ('others', 'Others'), ('rice', 'Rice'), ('bread', 'Bread')], default='others', max_length=20),
        ),
    ]
