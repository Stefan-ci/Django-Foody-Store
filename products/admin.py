from products.models import Item
from django.contrib import admin, messages
from django.utils.translation import gettext
from django.utils.translation import ngettext as _
from import_export.admin import ImportExportModelAdmin




class ItemAdmin(ImportExportModelAdmin):
	prepopulated_fields = {
		'slug' : ('title',),
	}
	list_display = ['title', 'is_public', 'price', 'discount_price',
		'date', 'category']
	list_filter = ['is_public', 'is_popular', 'date', 'category']
	
	actions = ['make_not_published', 'make_published', 
		'make_popular', 'make_not_popular']
	search_fields = ['title', 'tags__name', 'description', 'price', 
		'discount_price', 'category']


	"""
		Add custom actions to Model `Item`
	"""
	def make_published(self, request, queryset):
		updated = queryset.update(is_public=True)
		self.message_user(request, _(
				"%d plat a bien été marqué comme public",
				"%d plats ont bien été marqués comme publics",
				updated,
			) % updated, messages.SUCCESS)
	make_published.short_description = gettext("Marquer comme public")



	def make_not_published(self, request, queryset):
		updated = queryset.update(is_public=False)
		self.message_user(request, _(
				"%d plat a bien été marqué comme non-public",
				"%d plats ont bien été marqués comme non-publics",
				updated,
			) % updated, messages.SUCCESS)
	make_not_published.short_description = gettext("Marquer comme non-public")



	def make_popular(self, request, queryset):
		updated = queryset.update(is_popular=True)
		self.message_user(request, _(
				"%d plat a bien été marqué comme populaire",
				"%d plats ont bien été marqués comme populaires",
				updated,
			) % updated, messages.SUCCESS)
	make_popular.short_description = gettext("Marquer comme populaire")



	def make_not_popular(self, request, queryset):
		updated = queryset.update(is_popular=False)
		self.message_user(request, _(
				"%d plat a bien été marqué comme non-populaire",
				"%d plats ont bien été marqués comme non-populaires",
				updated,
			) % updated, messages.SUCCESS)
	make_not_popular.short_description = gettext("Marquer comme non-populaire")



admin.site.register(Item, ItemAdmin)



