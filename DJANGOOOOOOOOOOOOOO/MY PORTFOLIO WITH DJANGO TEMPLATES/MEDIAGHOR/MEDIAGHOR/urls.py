"""
URL configuration for MEDIAGHOR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('services', include(('Company_Services.urls', 'company_services'), namespace='company_services')),

    path('blogs', include(('Blog_Posts.urls', 'blogs'), namespace='blogs')),
    path('resources', include(('Resources.urls', 'resources'), namespace='resources')),
    path('subscribe', include(('subscriptions.urls', 'subscriptions'), namespace = 'subscriptions')),
    path('softwere', include(('Products.urls', 'products'), namespace = 'products')),
    path('sale', include(('sale.urls', 'sale'), namespace = 'sale')),
    path('', include(('management.urls', 'management'), namespace = 'management')),


    path('api/search-suggestions/', views.search_suggestions, name='search-suggestions'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
