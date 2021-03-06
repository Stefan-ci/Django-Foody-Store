# Generated by Django 3.2.5 on 2021-08-12 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, verbose_name='Adresse électronique')),
                ('subject', models.CharField(max_length=100, verbose_name='Sujet')),
                ('message', models.TextField(null=True, verbose_name='Message')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('is_answered', models.BooleanField(default=False, verbose_name='Traité')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
