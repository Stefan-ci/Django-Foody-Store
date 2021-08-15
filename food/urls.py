"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications.urls
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from django.contrib.sitemaps import GenericSitemap

from products.models import Item

info_dict = {
    'queryset' : Item.objects.filter(is_public=True),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
        
    path('', include('website.urls')),
    path('api/', include('api.urls')),

    path('superadmin/admin/', include('superadmin.urls')),


    path('sitemap.xml/', sitemap,
        {
            'sitemaps' : {
                'foods' : GenericSitemap(info_dict, priority=0.6),
            },
        },
        name='django.contrib.sitemaps.views.sitemap'),

    path('robots.txt/', TemplateView.as_view(
        template_name='robots.txt', 
        content_type='text/plain')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)

