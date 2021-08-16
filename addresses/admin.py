from django.contrib import admin
from addresses.models import Address
from import_export.admin import ImportExportModelAdmin


class AddressAdmin(ImportExportModelAdmin):
	list_display = ['user', 'street_address', 'apartment_address',
		'country', 'zip', 'address_type', 'default']
	list_filter = ['default']
	search_fields = ['user__username', 'street_address', 'country',
		'apartment_address', 'zip', 'address_type']

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

admin.site.register(Address, AddressAdmin)
