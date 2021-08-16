from profil.models import Profil
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

class ProfilAdmin(ImportExportModelAdmin):
	fieldsets = []
	list_display = ['user', 'stripe_customer_id', 'one_click_purchasing', 
		'date']
	list_filter = ['date', 'one_click_purchasing']
	search_fields = ['user__username', 'date', 'stripe_customer_id', 
		'one_click_purchasing']

	date_hierarchy = 'date'

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False


admin.site.register(Profil, ProfilAdmin)
