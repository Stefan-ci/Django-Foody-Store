# Generated by Django 3.2.5 on 2021-08-17 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_contact_unread'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='delete',
            field=models.BooleanField(default=False),
        ),
    ]
