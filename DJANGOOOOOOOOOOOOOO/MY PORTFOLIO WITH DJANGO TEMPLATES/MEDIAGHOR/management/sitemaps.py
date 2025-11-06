# management/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from Blog_Posts.models import BlogPost
from Resources.models import Library
from categories.models import LibraryCategory 


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.all()

    def location(self, obj):
        return f"/blogs/{obj.id}"  # adjust to your URL pattern


class ResourceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Library.objects.all()

    def location(self, obj):
        return f"/resources/{obj.id}"  # adjust if you use ID instead of slug


class ResourceCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 7.5

    def items(self):
        return LibraryCategory.objects.all()

    def location(self, obj):
        return f"/resources/category={obj.slug}"




class StaticViewSitemap(Sitemap):
    priority = 9
    changefreq = 'yearly'

    def items(self):
        return [
            'home',
            'about',
            'contact',
            'company_services:services',
            'blogs:all-posts',
            'resources:category_resources',
            'products:all_products'
        ]

    def location(self, item):
        return reverse(item)

