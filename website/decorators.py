from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages


def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			messages.warning(request, 'Désolé, vous êtes déjà connecté!')
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func




def admin_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if not request.user.is_superuser:
				return redirect('not-allowed')
			else:
				return view_func(request, *args, **kwargs)
	return wrapper_func




def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			
			if request.user.is_authenticated:
				if request.user.groups.exists():
					group = request.user.groups.all()[0].name
				if group in allowed_roles:
					return view_func(request, *args, **kwargs)
				else:
					return redirect('not-allowed')
			return redirect('login')
		return view_func
	return decorator
