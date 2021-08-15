from django.contrib import admin
from coupon.models import Coupon
from import_export.admin import ImportExportModelAdmin

class CouponAdmin(ImportExportModelAdmin):
	list_display = ['code', 'amount', 'end_date', 'is_active', 'date']
	list_filter = ['end_date', 'is_active', 'date']
	search_fields = ['code', 'amount']

admin.site.register(Coupon, CouponAdmin)