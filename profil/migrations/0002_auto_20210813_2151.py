# Generated by Django 3.2.5 on 2021-08-13 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profil',
            options={},
        ),
        migrations.AlterField(
            model_name='profil',
            name='one_click_purchasing',
            field=models.BooleanField(default=False),
        ),
    ]
