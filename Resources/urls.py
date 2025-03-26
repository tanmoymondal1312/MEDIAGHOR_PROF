from django.urls import path
from .views import click_on_copy

urlpatterns = [
    path('click_on_copy/', click_on_copy, name='click_on_copy'),
    # Add other blog URLs as needed...
]