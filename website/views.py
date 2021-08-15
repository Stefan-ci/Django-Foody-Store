from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, View, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, FormView
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.decorators import method_decorator
from django.db.models import Count

from rest_framework.response import Response
from rest_framework import serializers

import random
import string
import stripe


from products.models import Item
from coupon.models import Coupon
from orders.models import OrderItem, Order
from addresses.models import Address
from profil.models import Profil
from website.utils import update_views
from coupon.coupon_forms import CouponForm
from website.decorators import unauthenticated_user, admin_only, allowed_users
from profil.forms import CreateUserForm, EditUserForm
from contacts.forms import ContactForm
from refunds.models import Refund
from refunds.refund_forms import RefundForm
from orders.orders_forms import CheckoutForm
from payments.forms import PaymentForm


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_ref_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def is_valid_form(values):
	valid = True
	for field in values:
		if field == '':
			valid = False
	return valid




@login_required(login_url='login')
def not_allowed_view(request):
	context = {
		'current_site' : get_current_site(request),
	}
	template_name = 'not_allowed.html'
	return render(request, template_name, context)







# User login view
@unauthenticated_user
@csrf_protect
def login_view(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			if user.is_superuser:
				if 'next' in request.POST:

					messages.success(request, f"Welcome {username}")
					return redirect(request.POST.get('next'))
				else:
					messages.success(request,  f"Welcome {username}")
					return redirect('admin-home')
			else:
				if 'next' in request.POST:
					return redirect(request.POST.get('next'))
				else:
					return redirect('home')
		else:
			messages.warning(request, "Login attempt failed, try again !")
			return redirect('login')
	context = {
		'current_site' : get_current_site(request)
	}
	
	template_name = 'public/accounts/login.html'
	return render(request, template_name, context)






# User logout view
@login_required(login_url='login')
def logout_view(request):
	logout(request)
	messages.success(request, "Successfully logged out, Good bye !")
	return redirect('login')




# User register
class RegisterView(FormView):
	template_name = 'public/accounts/register.html'
	form_class = CreateUserForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('home')

	@method_decorator(unauthenticated_user)
	def dispatch(self, request, *args, **kwargs):
		return super(RegisterView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		user = form.save()
		user_name = form.cleaned_data.get('username')
		if user is not None:
			login(self.request, user)
		messages.success(self.request, f'Welcome {user_name}') 
		return super(RegisterView, self).form_valid(form)

	def get_context_data(self, **kwargs):
	
		context = super().get_context_data(**kwargs)
		context.update({
			'current_site' : get_current_site(self.request)
		})
		return context














def home_view(request):
	items = Item.objects.filter(is_public=True).order_by('-id')[:56]
	
	context = {
		'items' : items,
		'current_site' : get_current_site(request),
	}

	viewed_items = Item.objects.all()
	for item in viewed_items:
		update_views(request, item)

	template_name = 'public/home.html'
	return render(request, template_name, context)















@login_required
def add_food_to_cart(request, id, slug):
	public_item = Item.objects.filter(is_public=True)
	item = get_object_or_404(public_item, id=id, slug=slug)
	order_item, created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False
	)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if the order item is in the order
		if order.items.filter(item__id=item.id).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "This item quantity was updated.")
			return redirect("order-summary")
		else:
			order.items.add(order_item)
			messages.info(request, "This item was added to your cart.")
			return redirect("order-summary")
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(
			user=request.user, 
			ordered_date=ordered_date
		)
		order.items.add(order_item)
		messages.info(request, "This item was added to your cart.")
		return redirect("order-summary")













@login_required
def remove_food_from_cart(request, id, slug):
	public_item = Item.objects.filter(is_public=True)
	item = get_object_or_404(public_item, id=id, slug=slug)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False
	)
	if order_qs.exists():
		order = order_qs[0]
		# check if the order item is in the order
		if order.items.filter(item__id=item.id).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]
			order.items.remove(order_item)
			order_item.delete()
			messages.info(request, "This item was removed from your cart.")
			return redirect("order-summary")
		else:
			messages.info(request, "This item was not in your cart")
			return redirect("food-detail", id=id, slug=slug)
	else:
		messages.info(request, "You do not have an active order")
		return redirect("home")













@login_required
def remove_single_item_from_cart(request, id, slug):
	public_item = Item.objects.filter(is_public=True)
	item = get_object_or_404(public_item, id=id, slug=slug)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False
	)
	if order_qs.exists():
		order = order_qs[0]
		# check if the order item is in the order
		# check if the order item is in the order
		if order.items.filter(item__id=item.id).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False
			)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
				return redirect("order-summary")
			elif order_item.quantity == 1:
				OrderItem.objects.filter(
					item=item,
					user=request.user,
					ordered=False
				).delete()
				return redirect("order-summary")

			else:
				order.items.remove(order_item)
				messages.info(request, "This item quantity was updated.")
				return redirect("order-summary")
		else:
			messages.info(request, "This item was not in your cart, try to add it")
			return redirect("food-detail", id=id, slug=slug)
	else:
		messages.info(request, "You do not have an active order")
		return redirect("home")











def get_coupon(request, code):
	try:
		coupon = Coupon.objects.get(code=code) or None
		if coupon.is_active:
			return coupon
		else:
			messages.info(request, "Coupon is no more active")
			return redirect("order-summary")
	except ObjectDoesNotExist:
		messages.info(request, "Coupon does not exist")
		return redirect("order-summary")
















class AddCouponView(View):

	@method_decorator(login_required(login_url='login'))
	def dispatch(self, request, *args, **kwargs):
		return super(AddCouponView, self).dispatch(request, *args, **kwargs)

	def post(self, *args, **kwargs):
		form = CouponForm(self.request.POST or None)
		if form.is_valid():
			try:
				code = form.cleaned_data.get('code')
				order = Order.objects.get(
					user=self.request.user,
					ordered=False
				)
				order.coupon = get_coupon(self.request, code)
				order.save()
				messages.success(self.request, "Successfully added coupon")
				return redirect("checkout")
			except ObjectDoesNotExist:
				messages.info(self.request, "You do not have an active order")
				return redirect("food-list")












@login_required
def order_summary_view(request):
	order = Order.objects.get(user=request.user, ordered=False) or None
	context = {
		'order' : order,
		'current_site' : get_current_site(request),
	}

	template_name = 'public/orders/order_summary.html'
	return render(request, template_name, context)







def food_item_detail_view(request, id, slug):
	public_item = Item.objects.filter(is_public=True)
	item = get_object_or_404(public_item, id=id, slug=slug)

	# Trying to display simiralities with other items
	item_tags_ids = item.tags.values_list('id', flat=True)
	similar_items = Item.objects.filter(tags__in=item_tags_ids, is_public=True).exclude(id=item.id)
	similar_items = similar_items.annotate(same_tags=Count('tags')).order_by('-id')[:6]

	popular_items = Item.objects.filter(is_public=True, is_popular=True).exclude(id=item.id).order_by('-id')[:3]

	most_recent_items = Item.objects.filter(is_public=True).exclude(id=item.id).order_by('-id')[:5]

	update_views(request, item)
	
	
	context = {
		'item' : item,
		'popular_items' : popular_items,
		'similar_items' : similar_items,
		'most_recent_items' : most_recent_items,
		'current_site' : get_current_site(request),
	}

	
	template_name = 'public/items/item_detail.html'
	return render(request, template_name, context)












# Items list function based view
def food_item_list_view(request):

	if 'food' in request.GET:
		item = request.GET['food']
		items_list = Item.objects.filter(
			is_public=True,
			title__icontains=item).order_by('-id')
	else:
		items_list = Item.objects.filter(is_public=True).order_by('-id')

	
	paginator = Paginator(items_list, 100)
	page = request.GET.get("page")
	items_obj = paginator.get_page(page)

	try:
		items_list = paginator.page(page)
	except PageNotAnInteger:
		items_list = paginator.page(1)
	except EmptyPage:
		items_list = paginator.page(paginator.num_pages)
		
	context = {
		'items' : items_obj,
		'current_site' : get_current_site(request),
	}

	items = Item.objects.all()
	for item in items:
		update_views(request, item)
	
	template_name = 'public/items/items_list.html'
	return render(request, template_name, context)





def food_category_list_view(request, category):

	items = Item.objects.filter(category=category).order_by('-id')

	context = {
		'items' : items,
		'items_category' : category,
		'current_site' : get_current_site(request)
	}

	template_name = 'public/items/categories_list.html'
	return render(request, template_name, context)










def contact_us_view(request):
	contact_form = ContactForm

	# Contact on homepage
	if request.method == 'POST':
		contact_form = ContactForm(request.POST or None)
		if not contact_form.is_valid():
			messages.warning(request, "Feel entirely contact form please")
			return redirect(request.path_info)
		if contact_form.is_valid():
			form = contact_form.save(commit=False)
			form.is_answered = False
			form.save()

			contact_name = request.POST.get('contact_name')
			messages.success(request, "Thank for your message, we will answer soon")
			return redirect('home')


			name = request.POST.get('contact_name')
			email = request.POST.get('contact_email')
			subject = request.POST.get('contact_subject')
			message = request.POST.get('contact_message')

			# Send email to admin with contact message after contact form submited and saved.
			try:
				all_message = "Monsieur/Madame " + str(name) + " vous a contacté via votre portfolio. \n\n Son message est:\n\n" + str(message) + ".\n\n\n Merci de lui répondre dans les plus brefs délais!" + " \n\n Son adresse mail est: \t" + str(email) + "\n\n"
				subject = "Contact depuis le site " + str(get_current_site(request))
				from_email = settings.EMAIL_HOST_USER
				to_emails = ['kouassidiby7@gmail.com', 'claverdiby9@gmail.com',]           
				send_email = EmailMessage(
				    subject,
				    all_message,
				    from_email,
				    to_emails,
				)
				send_email.send(fail_silently=False)
			except:
				pass

			try:
				user_email = form.cleaned_data.get('contact_email')
				user_name = form.cleaned_data.get('contact_name')

				sending_email_subject = "Merci de nous avoir contacté !"
				sending_email_message = _(f"""
				Merci {user_name} de nous avoir contacté! Nous vous repondrons
				très prochainement.

				Merci et à bientôt !!!!!
				""")
				form.email_user(sending_email_subject, sending_email_message)
				return redirect('home')

			except:
				pass

	context = {
		'contact_form' : contact_form,
		'current_site' : get_current_site(request),
	}

	template_name = 'public/contact/contact.html'
	return render(request, template_name, context)









class RequestRefundView(View):
	
	@method_decorator(login_required(login_url='login'))
	def dispatch(self, request, *args, **kwargs):
		return super(RequestRefundView, self).dispatch(request, *args, **kwargs)

	def get(self, *args, **kwargs):
		form = RefundForm()
		context = {
			'form': form,
			'current_site' : get_current_site(self.request),
		}

		template_name = 'public/refunds/request_refund.html'
		return render(self.request, template_name, context)


	def post(self, *args, **kwargs):
		form = RefundForm(self.request.POST)
		if form.is_valid():
			ref_code = form.cleaned_data.get('ref_code')
			message = form.cleaned_data.get('message')
			email = form.cleaned_data.get('email')
			
			# edit the order
			try:
				order = Order.objects.get(ref_code=ref_code)
				order.refund_requested = True
				order.save()

				# store the refund
				refund = Refund()
				refund.order = order
				refund.reason = message
				refund.email = email
				refund.save()

				messages.info(self.request, "Your request was received.")
				return redirect('home')
			
			except ObjectDoesNotExist:
				messages.info(self.request, "This order does not exist.")
				return redirect("request-refund")







class CheckoutView(View):

	@method_decorator(login_required(login_url='login'))
	def dispatch(self, request, *args, **kwargs):
		return super(CheckoutView, self).dispatch(request, *args, **kwargs)

	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			form = CheckoutForm()
			context = {
				'form': form,
				'couponform': CouponForm(),
				'order': order,
				'DISPLAY_COUPON_FORM': True
			}

			shipping_address_qs = Address.objects.filter(
				user=self.request.user,
				address_type='S',
				default=True
			)
			billing_address_qs = Address.objects.filter(
				user=self.request.user,
				address_type='B',
				default=True
			)

			if shipping_address_qs.exists():
				context.update({
					'default_shipping_address': shipping_address_qs[0]
				})

			if billing_address_qs.exists():
				context.update({
					'default_billing_address': billing_address_qs[0]
				})



			template_name = 'public/orders/checkout_orders.html'
			return render(self.request, template_name, context)
		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an active order")
			return redirect("checkout")


	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			if form.is_valid():
				use_default_shipping = form.cleaned_data.get('use_default_shipping')
				if use_default_shipping:
					#print("Using the defualt shipping address")
					address_qs = Address.objects.filter(
						user=self.request.user,
						address_type='S',
						default=True
					)
					if address_qs.exists():
						shipping_address = address_qs[0]
						order.shipping_address = shipping_address
						order.save()
					else:
						messages.info(self.request, "No default shipping address available")
						return redirect('checkout')
				
				else:
					#print("User is entering a new shipping address")
					shipping_address1 = form.cleaned_data.get('shipping_address')
					shipping_address2 = form.cleaned_data.get('shipping_address2')
					shipping_country = form.cleaned_data.get('shipping_country')
					shipping_zip = form.cleaned_data.get('shipping_zip')

					if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
						shipping_address = Address(
							user=self.request.user,
							street_address=shipping_address1,
							apartment_address=shipping_address2,
							country=shipping_country,
							zip=shipping_zip,
							address_type='S'
						)
						shipping_address.save()

						order.shipping_address = shipping_address
						order.save()

						set_default_shipping = form.cleaned_data.get('set_default_shipping')
						if set_default_shipping:
							shipping_address.default = True
							shipping_address.save()
					else:
						messages.info(self.request, "Please fill in the required shipping address fields")
						return redirect('checkout')


				use_default_billing = form.cleaned_data.get('use_default_billing')
				same_billing_address = form.cleaned_data.get('same_billing_address')

				if same_billing_address:
					billing_address = shipping_address
					billing_address.pk = None
					billing_address.save()
					billing_address.address_type = 'B'
					billing_address.save()
					order.billing_address = billing_address
					order.save()
				elif use_default_billing:
					#print("Using the defualt billing address")
					address_qs = Address.objects.filter(
						user=self.request.user,
						address_type='B',
						default=True
					)
					if address_qs.exists():
						billing_address = address_qs[0]
						order.billing_address = billing_address
						order.save()
					else:
						messages.info(self.request, "No default billing address available")
						return redirect('checkout')

				else:
					print("User is entering a new billing address")
					billing_address1 = form.cleaned_data.get('billing_address')
					billing_address2 = form.cleaned_data.get('billing_address2')
					billing_country = form.cleaned_data.get('billing_country')
					billing_zip = form.cleaned_data.get('billing_zip')

					if is_valid_form([billing_address1, billing_country, billing_zip]):
						billing_address = Address(
							user=self.request.user,
							street_address=billing_address1,
							apartment_address=billing_address2,
							country=billing_country,
							zip=billing_zip,
							address_type='B'
						)
						billing_address.save()

						order.billing_address = billing_address
						order.save()

						set_default_billing = form.cleaned_data.get('set_default_billing')
						if set_default_billing:
							billing_address.default = True
							billing_address.save()

					else:
						messages.info(self.request, "Please fill in the required shipping address fields")
						return redirect('checkout')


				payment_option = form.cleaned_data.get('payment_option')
				if payment_option == 'S':
					return redirect('payment', payment_option='stripe')
				elif payment_option == 'P':
					return redirect('payment', payment_option='paypal')
				else:
					messages.warning(self.request, "Invalid payment option selected")
					return redirect('checkout')


		except ObjectDoesNotExist:
			messages.warning(self.request, "You do not have an active order")
			return redirect("order-summary")














class PaymentView(View):

	@method_decorator(login_required(login_url='login'))
	def dispatch(self, request, *args, **kwargs):
		return super(PaymentView, self).dispatch(request, *args, **kwargs)

	def get(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		if order.billing_address:
			context = {
				'order': order,
				'DISPLAY_COUPON_FORM': False,
				'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
			}
			userprofile = self.request.user.profil
			if userprofile.one_click_purchasing:
				cards = stripe.Customer.list_sources(
					userprofile.stripe_customer_id,
					limit=3,
					object='card'
				)
				card_list = cards['data']
				if len(card_list) > 0:
					# update the context with the default card
					context.update({
						'card': card_list[0]
					})

			template_name = 'public/payment/payment.html'
			return render(self.request, template_name, context)

		else:
			messages.warning(self.request, "You have not added a billing address")
			return redirect('checkout')


	def post(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		form = PaymentForm(self.request.POST)
		userprofile = Profil.objects.get(user=self.request.user)
		if form.is_valid():
			token = form.cleaned_data.get('stripeToken')
			save = form.cleaned_data.get('save')
			use_default = form.cleaned_data.get('use_default')

			if save:
				if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
					customer = stripe.Customer.retrieve(userprofile.stripe_customer_id)
					customer.sources.create(source=token)

				else:
					customer = stripe.Customer.create(
						email=self.request.user.email,
					)
					customer.sources.create(source=token)
					userprofile.stripe_customer_id = customer['id']
					userprofile.one_click_purchasing = True
					userprofile.save()

			amount = int(order.get_total() * 100)

			try:
				if use_default or save:
					# charge the customer because we cannot charge the token more than once
					charge = stripe.Charge.create(
						amount=amount,  # cents
						currency="usd",
						customer=userprofile.stripe_customer_id
					)
				else:
					# charge once off on the token
					charge = stripe.Charge.create(
						amount=amount,  # cents
						currency="usd",
						source=token
					)


				# create the payment
				payment = Payment()
				payment.stripe_charge_id = charge['id']
				payment.user = self.request.user
				payment.amount = order.get_total()
				payment.save()

				# assign the payment to the order

				order_items = order.items.all()
				order_items.update(ordered=True)
				for item in order_items:
					item.save()


				order.ordered = True
				order.payment = payment
				order.ref_code = create_ref_code()
				order.save()

				messages.success(self.request, "Your order was successful!")
				return redirect("home")


			except stripe.error.CardError as e:
				body = e.json_body
				err = body.get('error', {})
				messages.warning(self.request, f"{err.get('message')}")
				return redirect("home")

			except stripe.error.RateLimitError as e:
				# Too many requests made to the API too quickly
				messages.warning(self.request, "Rate limit error")
				return redirect("home")

			except stripe.error.InvalidRequestError as e:
				# Invalid parameters were supplied to Stripe's API
				print(e)
				messages.warning(self.request, "Invalid parameters")
				return redirect("home")

			except stripe.error.AuthenticationError as e:
				# Authentication with Stripe's API failed
				# (maybe you changed API keys recently)
				messages.warning(self.request, "Not authenticated")
				return redirect("home")

			except stripe.error.APIConnectionError as e:
				# Network communication with Stripe failed
				messages.warning(self.request, "Network error")
				return redirect("home")

			except stripe.error.StripeError as e:
				# Display a very generic error to the user, and maybe send
				# yourself an email
				messages.warning(
				self.request, "Something went wrong. You were not charged. Please try again.")
				return redirect("home")

			except Exception as e:
				# send an email to ourselves
				messages.warning(
				self.request, "A serious error occurred. We have been notifed.")
				return redirect("home")

		messages.warning(self.request, "Invalid data received")
		return redirect("payment", payment_option='stripe')








