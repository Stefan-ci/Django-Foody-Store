from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, View, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, FormView
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.urls import reverse_lazy


from django.core.exceptions import ObjectDoesNotExist
from hitcount.views import HitCountDetailView
from notifications.models import Notification
from notifications import settings as notif_settings
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives


from hitcount.models import HitCount, Hit


from datetime import datetime
date = datetime.now()
curr_month = date.month
curr_year = date.year



from products.models import Item
from coupon.models import Coupon
from contacts.models import Contact
from orders.models import OrderItem, Order
from addresses.models import Address
from profil.models import Profil
from reports.models import Sales, Expenses
from payments.models import Payment
from website.utils import update_views
from reports.reports_utils import expenses_made, sales_made, monthly_sales, monthly_expenses
from coupon.coupon_forms import CouponForm
from website.decorators import unauthenticated_user, admin_only, allowed_users
from profil.forms import CreateUserForm, EditUserForm
from contacts.forms import ContactForm
from refunds.models import Refund
from refunds.refund_forms import RefundForm
from orders.orders_forms import CheckoutForm
from payments.forms import PaymentForm
from superadmin.utils import daily_visits




@login_required(login_url='login')
@admin_only
def mark_all_as_delete(request):
	notifications = Notification.objects.filter(recipient=request.user)
	for notification in notifications:
		if notif_settings.get_config()['SOFT_DELETE']:
			notification.deleted = True
			notification.save()
		else:
			notification.delete()
	_next = request.GET.get('next')
	if _next:
		return redirect(_next)
	return redirect('admin-inbox')




@login_required(login_url='login')
@admin_only
def mark_as_delivered(request, id):
	order = get_object_or_404(Order, id=id)
	order.being_delivered = True
	order.save()
	messages.success(request, 'Order successfully marked as delivered !!!')
	_next = request.GET.get('next')
	if _next:
		return redirect(_next)
	return redirect('order-not-delivered')


@login_required(login_url='login')
@admin_only
def mark_as_received(request, id):
	order = get_object_or_404(Order, id=id)
	order.received = True
	order.save()
	messages.success(request, 'Order successfully marked as received !!!')
	_next = request.GET.get('next')
	if _next:
		return redirect(_next)
	return redirect('order-not-received')




@login_required(login_url='login')
@admin_only
def mark_contact_as_deleted(request, id):
	contact = get_object_or_404(Contact, id=id)
	contact.deleted = True
	contact.save()
	messages.success(request, 'Message successfully marked as deleted !!!')
	_next = request.GET.get('next')
	if _next:
		return redirect(_next)
	return redirect('new-messages')


@login_required(login_url='login')
@admin_only
def mark_contact_as_read(request, id):
	contact = get_object_or_404(Contact, id=id)
	contact.unread = False
	contact.is_answered = True
	contact.save()
	messages.success(request, 'Message successfully marked as read & answered !!!')
	_next = request.GET.get('next')
	if _next:
		return redirect(_next)
	return redirect('new-messages')







not_granted_refunds_count = Refund.objects.filter(
	accepted=False).count()
all_refunds_list = Refund.objects.all()
all_refunds_count = Refund.objects.all().count()



unread_contacts_count = Contact.objects.filter(
	unread=True,
	is_answered=False,
	deleted=False).count()
unread_contacts_nav_list = Contact.objects.filter(
	unread=True,
	is_answered=False,
	deleted=False)[:10]
unread_contacts_list = Contact.objects.filter(
	unread=True,
	is_answered=False,
	deleted=False)[:50]



not_received_orders_count = Order.objects.filter(
	ordered=True,
	being_delivered=True,
	received=False,
).count()
not_delivered_orders_count = Order.objects.filter(
	ordered=True,
	being_delivered=False,
	received=False,
).count()




complete_orders_list = Order.objects.filter(ordered=True)
complete_orders_count = Order.objects.filter(ordered=True).count()

not_complete_orders_list = Order.objects.filter(ordered=False)
not_complete_orders_count = Order.objects.filter(ordered=False).count()

total_hits = Hit.objects.all().count()

new_added_items_count = Item.objects.filter(date__month=8).count()

total_items_count = Item.objects.all().count()

lambda_users_count = User.objects.filter(is_staff=False).count()
superusers_count = User.objects.filter(is_superuser=True).count()
staff_users_count = User.objects.filter(is_staff=True).count()
users_count = User.objects.all().count()

orders_list = Order.objects.all().order_by('-id')[:100]
total_orders_count = Order.objects.filter(ordered=True).count()


# Sales' annual chart reports data (getting by month)
# Sale means that payment done successfully. So we will work with `Payment` model
jan_sale = Payment.objects.filter(date__month=1).count()
feb_sale = Payment.objects.filter(date__month=2).count()
march_sale = Payment.objects.filter(date__month=3).count()
apr_sale = Payment.objects.filter(date__month=4).count()
may_sale = Payment.objects.filter(date__month=5).count()
jun_sale = Payment.objects.filter(date__month=6).count()
jul_sale = Payment.objects.filter(date__month=7).count()
aug_sale = Payment.objects.filter(date__month=8).count()
sept_sale = Payment.objects.filter(date__month=9).count()
oct_sale = Payment.objects.filter(date__month=10).count()
nov_sale = Payment.objects.filter(date__month=11).count()
dec_sale = Payment.objects.filter(date__month=12).count()




jan_expense = Expenses.objects.filter(date__month=1).count()
feb_expense = Expenses.objects.filter(date__month=2).count()
march_expense = Expenses.objects.filter(date__month=3).count()
apr_expense = Expenses.objects.filter(date__month=4).count()
may_expense = Expenses.objects.filter(date__month=5).count()
jun_expense = Expenses.objects.filter(date__month=6).count()
jul_expense = Expenses.objects.filter(date__month=7).count()
aug_expense = Expenses.objects.filter(date__month=8).count()
sept_expense = Expenses.objects.filter(date__month=9).count()
oct_expense = Expenses.objects.filter(date__month=10).count()
nov_expense = Expenses.objects.filter(date__month=11).count()
dec_expense = Expenses.objects.filter(date__month=12).count()






# Users' annual chart reports data (getting by month)
jan_user = User.objects.filter(date_joined__month=1).count()
feb_user = User.objects.filter(date_joined__month=2).count()
march_user = User.objects.filter(date_joined__month=3).count()
apr_user = User.objects.filter(date_joined__month=4).count()
may_user = User.objects.filter(date_joined__month=5).count()
jun_user = User.objects.filter(date_joined__month=6).count()
jul_user = User.objects.filter(date_joined__month=7).count()
aug_user = User.objects.filter(date_joined__month=8).count()
sept_user = User.objects.filter(date_joined__month=9).count()
oct_user = User.objects.filter(date_joined__month=10).count()
nov_user = User.objects.filter(date_joined__month=11).count()
dec_user = User.objects.filter(date_joined__month=12).count()



total_sales_made = sales_made()
total_expenses_made = expenses_made()
total_profits_made = total_sales_made - total_expenses_made










@login_required(login_url='login')
@admin_only
def admin_home_view(request):
	
	context = {
		'not_received_orders_count' : not_received_orders_count,
		'not_delivered_orders_count' : not_delivered_orders_count,
		'total_orders_count' : total_orders_count,


		'unread_contacts_count' : unread_contacts_count,
		'unread_contacts_list' : unread_contacts_list,
		'unread_contacts_nav_list' : unread_contacts_nav_list,

		'all_refunds_list' : all_refunds_list,
		'all_refunds_count' : all_refunds_count,
		'not_granted_refunds_count' : not_granted_refunds_count,



		'jan_sale' : jan_sale,
		'feb_sale' : feb_sale,
		'march_sale' : march_sale,
		'apr_sale' : apr_sale,
		'may_sale' : may_sale,
		'jun_sale' : jun_sale,
		'jul_sale' : jun_sale,
		'aug_sale' : aug_sale,
		'sept_sale' : sept_sale,
		'oct_sale' : oct_sale,
		'nov_sale' : nov_sale,
		'dec_sale' : dec_sale,

		'jan_expense' : jan_expense,
		'feb_expense' : feb_expense,
		'march_expense' : march_expense,
		'apr_expense' : apr_expense,
		'may_expense' : may_expense,
		'jun_expense' : jun_expense,
		'jul_expense' : jun_expense,
		'aug_expense' : aug_expense,
		'sept_expense' : sept_expense,
		'oct_expense' : oct_expense,
		'nov_expense' : nov_expense,
		'dec_expense' : dec_expense,

		'jan_user' : jan_user,
		'feb_user' : feb_user,
		'march_user' : march_user,
		'apr_user' : apr_user,
		'may_user' : may_user,
		'jun_user' : jun_user,
		'jul_user' : jun_user,
		'aug_user' : aug_user,
		'sept_user' : sept_user,
		'oct_user' : oct_user,
		'nov_user' : nov_user,
		'dec_user' : dec_user,


		'mon_visits' : daily_visits(1, curr_month, curr_year),
		'tue_visits' : daily_visits(2, curr_month, curr_year),
		'wed_visits' : daily_visits(3, curr_month, curr_year),
		'thus_visits' : daily_visits(4, curr_month, curr_year),
		'fri_visits' : daily_visits(5, curr_month, curr_year),
		'sat_visits' : daily_visits(6, curr_month, curr_year),
		'sun_visits' : daily_visits(7, curr_month, curr_year),


		'jan_sale_amount' : monthly_sales(1),
		'feb_sale_amount' : monthly_sales(2),
		'march_sale_amount' : monthly_sales(3),
		'apr_sale_amount' : monthly_sales(4),
		'may_sale_amount' : monthly_sales(5),
		'jun_sale_amount' : monthly_sales(6),
		'jul_sale_amount' : monthly_sales(7),
		'aug_sale_amount' : monthly_sales(8),
		'sept_sale_amount' : monthly_sales(9),
		'oct_sale_amount' : monthly_sales(10),
		'nov_sale_amount' : monthly_sales(11),
		'dec_sale_amount' : monthly_sales(12),



		'jan_expense_amount' : monthly_expenses(1),
		'feb_expense_amount' : monthly_expenses(2),
		'march_expense_amount' : monthly_expenses(3),
		'apr_expense_amount' : monthly_expenses(4),
		'may_expense_amount' : monthly_expenses(5),
		'jun_expense_amount' : monthly_expenses(6),
		'jul_expense_amount' : monthly_expenses(7),
		'aug_expense_amount' : monthly_expenses(8),
		'sept_expense_amount' : monthly_expenses(9),
		'oct_expense_amount' : monthly_expenses(10),
		'nov_expense_amount' : monthly_expenses(11),
		'dec_expense_amount' : monthly_expenses(12),

		'total_hits' : total_hits,
		'users_count' : users_count,
		'total_sales_made' : total_sales_made,
		'total_profits_made' : total_profits_made,
		'superusers_count' : superusers_count,
		'total_expenses_made' : total_expenses_made,
		'total_items_count' : total_items_count,
		'staff_users_count' : staff_users_count,
		'lambda_users_count' : lambda_users_count,
		'current_site' : get_current_site(request),
		'complete_orders_count' : complete_orders_count,
		'new_added_items_count' : new_added_items_count,
		'not_complete_orders_count' : not_complete_orders_count,
		'orders_list' : Order.objects.filter(ordered=True,received=False).order_by('-id')[:5],
	}

	template_name = 'admin/admin_home.html'
	return render(request, template_name, context)












@login_required(login_url='login')
@admin_only
def not_received_orders_list_view(request):

	if 'search' in request.GET:
		search_order = request.GET['search']
		orders_list = Order.objects.filter(
			ordered=True,
			received=False,
			being_delivered=True,
			user__username__icontains=search_order,
		).order_by('-id')[:100]
	else:
		orders_list = Order.objects.filter(
			ordered=True,
			received=False,
			being_delivered=True,).order_by('-id')[:100]

	paginator = Paginator(orders_list, 100)
	page = request.GET.get("page")
	orders_obj = paginator.get_page(page)

	try:
		orders_list = paginator.page(page)
	except PageNotAnInteger:
		orders_list = paginator.page(1)
	except EmptyPage:
		orders_list = paginator.page(paginator.num_pages)
		

	context = {
		'orders_list' : orders_obj,


		'not_received_orders_count' : not_received_orders_count,
		'current_site' : get_current_site(request),
		'not_delivered_orders_count' : not_delivered_orders_count,
		'total_orders_count' : total_orders_count,

		'all_refunds_list' : all_refunds_list,
		'all_refunds_count' : all_refunds_count,
		'not_granted_refunds_count' : not_granted_refunds_count,


		'unread_contacts_count' : unread_contacts_count,
		'unread_contacts_list' : unread_contacts_list,
		'unread_contacts_nav_list' : unread_contacts_nav_list,

	}

	template_name = 'admin/orders/not_received_orders.html'
	return render(request, template_name, context)










@login_required(login_url='login')
@admin_only
def not_delivered_orders_list_view(request):

	if 'search' in request.GET:
		search_order = request.GET['search']
		orders_list = Order.objects.filter(
			ordered=True,
			received=False,
			being_delivered=False,
			user__username__icontains=search_order,
		).order_by('-id')[:100]
	else:
		orders_list = Order.objects.filter(
			ordered=True,
			received=False,
			being_delivered=False,).order_by('-id')[:100]

	paginator = Paginator(orders_list, 100)
	page = request.GET.get("page")
	orders_obj = paginator.get_page(page)

	try:
		orders_list = paginator.page(page)
	except PageNotAnInteger:
		orders_list = paginator.page(1)
	except EmptyPage:
		orders_list = paginator.page(paginator.num_pages)
		

	context = {
		'orders_list' : orders_obj,
		

		'not_received_orders_count' : not_received_orders_count,
		'current_site' : get_current_site(request),
		'not_delivered_orders_count' : not_delivered_orders_count,
		'total_orders_count' : total_orders_count,

		'all_refunds_list' : all_refunds_list,
		'all_refunds_count' : all_refunds_count,
		'not_granted_refunds_count' : not_granted_refunds_count,

		'unread_contacts_count' : unread_contacts_count,
		'unread_contacts_list' : unread_contacts_list,
		'unread_contacts_nav_list' : unread_contacts_nav_list,

	}

	template_name = 'admin/orders/not_delivered_orders.html'
	return render(request, template_name, context)
















@login_required(login_url='login')
@admin_only
def all_orders_list_view(request):

	if 'search' in request.GET:
		search_order = request.GET['search']
		orders_list = Order.objects.filter(
			ordered=True,
			user__username__icontains=search_order,
		).order_by('-id')[:100]
	else:
		orders_list = Order.objects.filter(
			ordered=True).order_by('-id')[:100]

	paginator = Paginator(orders_list, 100)
	page = request.GET.get("page")
	orders_obj = paginator.get_page(page)

	try:
		orders_list = paginator.page(page)
	except PageNotAnInteger:
		orders_list = paginator.page(1)
	except EmptyPage:
		orders_list = paginator.page(paginator.num_pages)
		

	context = {
		'orders_list' : orders_obj,
		

		'not_received_orders_count' : not_received_orders_count,
		'current_site' : get_current_site(request),
		'not_delivered_orders_count' : not_delivered_orders_count,
		'total_orders_count' : total_orders_count,

		'all_refunds_list' : all_refunds_list,
		'all_refunds_count' : all_refunds_count,
		'not_granted_refunds_count' : not_granted_refunds_count,

		'unread_contacts_count' : unread_contacts_count,
		'unread_contacts_list' : unread_contacts_list,
		'unread_contacts_nav_list' : unread_contacts_nav_list,
	}

	template_name = 'admin/orders/all_orders_list.html'
	return render(request, template_name, context)












@login_required(login_url='login')
@admin_only
def order_detail_view(request, id):
	# order_made = Order.objects.filter(ordered=True)
	# order = get_object_or_404(order_made, id=id)

	order = get_object_or_404(Order, id=id)

	context = {
		'order' : order,


		'not_received_orders_count' : not_received_orders_count,
		'current_site' : get_current_site(request),
		'not_delivered_orders_count' : not_delivered_orders_count,
		'total_orders_count' : total_orders_count,

		'all_refunds_list' : all_refunds_list,
		'all_refunds_count' : all_refunds_count,
		'not_granted_refunds_count' : not_granted_refunds_count,

		'unread_contacts_count' : unread_contacts_count,
		'unread_contacts_list' : unread_contacts_list,
		'unread_contacts_nav_list' : unread_contacts_nav_list,
	}

	template_name = 'admin/orders/order_detail.html'
	return render(request, template_name, context)


















@login_required(login_url='login')
@admin_only
def admin_inbox_view(request):
	
	context = {
		'not_received_orders_count' : not_received_orders_count,
		'current_site' : get_current_site(request),
		'not_delivered_orders_count' : not_delivered_orders_count,
		'total_orders_count' : total_orders_count,

		'all_refunds_list' : all_refunds_list,
		'all_refunds_count' : all_refunds_count,
		'not_granted_refunds_count' : not_granted_refunds_count,

		'unread_contacts_count' : unread_contacts_count,
		'unread_contacts_list' : unread_contacts_list,
		'unread_contacts_nav_list' : unread_contacts_nav_list,
	}

	template_name = 'admin/inbox/admin_inbox.html'
	return render(request, template_name, context)













def new_messages_list_view(request):

	if 'search' in request.GET:
		search = request.GET['search']
		unread_contacts_list = Contact.objects.filter(
			unread=True,
			is_answered=False,
			deleted=False,
			name__icontains=search,
		).order_by('-id')[:100]
	else:
		unread_contacts_list = Contact.objects.filter(
			unread=True,
			is_answered=False,
			deleted=False,).order_by('-id')[:100]

	paginator = Paginator(unread_contacts_list, 100)
	page = request.GET.get("page")
	orders_obj = paginator.get_page(page)

	try:
		unread_contacts_list = paginator.page(page)
	except PageNotAnInteger:
		unread_contacts_list = paginator.page(1)
	except EmptyPage:
		unread_contacts_list = paginator.page(paginator.num_pages)

	context = {
		'not_received_orders_count' : not_received_orders_count,
		'current_site' : get_current_site(request),
		'not_delivered_orders_count' : not_delivered_orders_count,
		'total_orders_count' : total_orders_count,

		'all_refunds_list' : all_refunds_list,
		'all_refunds_count' : all_refunds_count,
		'not_granted_refunds_count' : not_granted_refunds_count,

		'unread_contacts_count' : unread_contacts_count,
		'unread_contacts_list' : unread_contacts_list,
		'unread_contacts_nav_list' : unread_contacts_nav_list,
	}

	template_name = 'admin/messages/new_messages.html'
	return render(request, template_name, context)











