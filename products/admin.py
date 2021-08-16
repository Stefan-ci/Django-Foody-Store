from products.models import Item
from django.contrib import admin, messages
from django.utils.translation import ngettext as _
from import_export.admin import ImportExportModelAdmin




class ItemAdmin(ImportExportModelAdmin):
	prepopulated_fields = {
		'slug' : ('title',),
	}
	list_display = ['title', 'is_public', 'price', 'discount_price',
		'date', 'category', 'is_popular']
	list_filter = ['is_public', 'is_popular', 'date', 'category']
	
	actions = ['make_not_published', 'make_published', 
		'make_popular', 'make_not_popular']
	search_fields = ['title', 'tags__name', 'description', 'price', 
		'discount_price', 'category']

	date_hierarchy = 'date'

	

	def has_delete_permission(self, request, obj=None):
		return False


	"""
		Add custom actions to Model `Item`
	"""
	def make_published(self, request, queryset):
		updated = queryset.update(is_public=True)
		self.message_user(request, _(
				"%d item marked as public",
				"%d items marked as public",
				updated,
			) % updated, messages.SUCCESS)
	make_published.short_description = 'Mark as public'



	def make_not_published(self, request, queryset):
		updated = queryset.update(is_public=False)
		self.message_user(request, _(
				"%d item marked as not public",
				"%d items marked as not public",
				updated,
			) % updated, messages.SUCCESS)
	make_not_published.short_description = 'Mark as not public'



	def make_popular(self, request, queryset):
		updated = queryset.update(is_popular=True)
		self.message_user(request, _(
				"%d item marked as popular",
				"%d items marked as popular",
				updated,
			) % updated, messages.SUCCESS)
	make_popular.short_description = 'Mark as popular'



	def make_not_popular(self, request, queryset):
		updated = queryset.update(is_popular=False)
		self.message_user(request, _(
				"%d item marked as not popular",
				"%d items marked as not popular",
				updated,
			) % updated, messages.SUCCESS)
	make_not_popular.short_description = 'Mark as not popular'



admin.site.register(Item, ItemAdmin)



