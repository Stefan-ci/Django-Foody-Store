# Generated by Django 3.2.5 on 2021-08-12 21:39

from django.db import migrations, models
import django_resized.forms
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Titre')),
                ('slug', models.SlugField(help_text='Le remplissage de ce champs est automatique', max_length=400, verbose_name="Lien d'accès")),
                ('description', models.TextField(help_text='Description du plat à ajouter')),
                ('picture', django_resized.forms.ResizedImageField(crop=None, force_format=None, help_text="Chargez l'image principale ici", keep_meta=True, quality=100, size=[500, 500], upload_to='images/foods/%Y/%m/', verbose_name='Image principale')),
                ('is_public', models.BooleanField(default=True, verbose_name='Public')),
                ('picture_2', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, help_text="Chargez l'image secondaire ici", keep_meta=True, null=True, quality=100, size=[500, 500], upload_to='images/foods/%Y/%m/', verbose_name='Image 2')),
                ('picture_3', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, help_text='Chargez une troisième image ici', keep_meta=True, null=True, quality=100, size=[500, 500], upload_to='images/foods/%Y/%m/', verbose_name='Image 3')),
                ('is_popular', models.BooleanField(default=False, verbose_name='Populaire')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField(verbose_name='Prix')),
                ('discount_price', models.FloatField(blank=True, help_text='Il doit être supérieur au prix (Prix sans réduction)', null=True, verbose_name='Prix normal')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Plat',
                'verbose_name_plural': 'Plats',
            },
        ),
    ]