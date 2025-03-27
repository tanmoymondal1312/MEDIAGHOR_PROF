from django.urls import path
from .views import click_on_copy,single_category_resources

urlpatterns = [
    path('click_on_copy/', click_on_copy, name='click_on_copy'),
    path('<slug:resourcesName>/', single_category_resources, name='single_category_resources'),

    # Add other blog URLs as needed...
]