from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogSitemap, ResourceSitemap, StaticViewSitemap, ResourceCategorySitemap

sitemaps = {
    'blogs': BlogSitemap,
    'resources': ResourceSitemap,
    'categories': ResourceCategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
