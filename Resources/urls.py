from django.urls import path
from .views import click_on_copy,single_category_resources,library

urlpatterns = [
    path('/click_on_copy/', click_on_copy, name='click_on_copy'),
    path('', single_category_resources, name='category_resources'),
    path('/category=<slug:resourcesName>', single_category_resources, name='single_category_resources'),
    path('/<str:id>', library, name='library_detail'),


    # Add other blog URLs as needed...
]