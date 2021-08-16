from orders.models import Order, OrderItem
from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.utils.translation import gettext as _
from import_export.admin import ImportExportModelAdmin




class OrderAdmin(ImportExportModelAdmin):
	list_display = ['user', 'start_date', 'ordered_date', 'ordered',
		'shipping_address', 'billing_address', 'payment', 'coupon',
		'being_delivered', 'received', 'refund_requested', 
		'refund_granted']
	list_filter = ['start_date', 'ordered_date', 'ordered', 
		'being_delivered', 'received', 'refund_requested', 
		'refund_granted']
	search_fields = ['user__username', 'start_date', 'ordered_date', 
		'shipping_address', 'billing_address', 'payment', 'coupon',
		'being_delivered', 'received', 'refund_requested', 
		'refund_granted', 'ordered',]
	list_display_links = ['user', 'shipping_address', 'coupon',
		'billing_address', 'payment',]
	actions = ['make_refund_accepted']
	date_hierarchy = 'ordered_date'

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False


	def make_refund_accepted(self, request, queryset):
		updated = queryset.update(
			refund_requested=False, 
			refund_granted=True)
		self.message_user(request, ngettext(
				"%d refund accepted successfully",
				"%d refunds accepted successfully",
				updated,
			) % updated, messages.SUCCESS)
	text = _('Update orders to refund granted')
	make_refund_accepted.short_description = text



class OrderItemAdmin(ImportExportModelAdmin):
	list_display = ['user', 'ordered', 'item', 'quantity', 'date']
	list_filter = ['date', 'ordered']
	search_fields = ['user__username', 'item__title', 'quantity']

	date_hierarchy = 'date'

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)