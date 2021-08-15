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
from django.db.models import Q


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.urls import reverse_lazy


from django.core.exceptions import ObjectDoesNotExist
from hitcount.views import HitCountDetailView
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives


from website.decorators import unauthenticated_user, admin_only, allowed_users





lambda_users_count = User.objects.filter(is_staff=False).count()
superusers_count = User.objects.filter(is_superuser=True).count()
staff_users_count = User.objects.filter(is_staff=True).count()
users_count = User.objects.all().count()



@login_required(login_url='login')
@admin_only
def admin_home_view(request):
	
	context = {
		'users_count' : users_count,
		'superusers_count' : superusers_count,
		'staff_users_count' : staff_users_count,
		'lambda_users_count' : lambda_users_count,
		'current_site' : get_current_site(request),
	}

	template_name = 'admin/admin_home.html'
	return render(request, template_name, context)


