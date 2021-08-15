from django.db import models
from django.urls import reverse
from hitcount.models import HitCount
from taggit.managers import TaggableManager
from django_resized import ResizedImageField
from django.contrib.contenttypes.fields import GenericRelation



CATEGORY_CHOICES = (
    ('steak', 'Steak'),
    ('vegan', 'Vegan'),
    ('vegetarian', 'Vegetarian'),
    ('rice', 'Rice'),
    ('bread', 'Bread'),
    ('asian', 'Asian'),
    ('american', 'American'),
    ('european', 'European'),
    ('australian', 'Australian'),
    ('african', 'African'),
    ('chenese', 'Chenese'),
    ('vietnamian', 'Vietnamian'),
    ('others', 'Others'),
)

class Item(models.Model):
	hit_count_generic = GenericRelation(HitCount, 
		object_id_field='object_pk',
		related_query_name='hit_count_generic_relation'
	)
	title = models.CharField(max_length=255)
	slug = models.SlugField( max_length=400, 
		help_text='Autofill field')
	description = models.TextField()
	picture = ResizedImageField(
		size=[500, 500],
		quality=100,
		upload_to='images/foods/%Y/%m/',
		help_text="Main picture")
	tags = TaggableManager()
	is_public = models.BooleanField(default=True)
	picture_2 = ResizedImageField(
		size=[500, 500],
		quality=100,
		null=True,
		blank=True,
		upload_to='images/foods/%Y/%m/',
		help_text="Second picture")
	picture_3 = ResizedImageField(
		size=[500, 500],
		quality=100,
		null=True,
		blank=True,
		upload_to='images/foods/%Y/%m/',
		help_text="Third picture")
	is_popular = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	price = models.FloatField()
	discount_price = models.FloatField(blank=True, null=True, 
		help_text='Must be smaller than normal price')
	category = models.CharField(max_length=20, default='others',
		choices=CATEGORY_CHOICES)
	
	def __str__(self):
		return str(self.title)

	def get_absolute_url(self):
		return reverse('food-detail', kwargs={
			"id" : self.id,
			"slug" : self.slug,
		})

	def get_add_to_cart_url(self):
		return reverse("add-food-to-cart", kwargs={
			"id" : self.id,
			"slug" : self.slug,
		})

	def get_remove_from_cart_url(self):
		return reverse("remove-food-from-cart", kwargs={
			"id" : self.id,
			"slug" : self.slug,
		})