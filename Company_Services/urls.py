from django.urls import path
from .import views

urlpatterns = [
    path('', views.services, name='services'),
    path('/<str:id>', views.service, name='service_details'),
    path('/<str:id>/contact', views.service, {'contact': 'contact'}, name='service_details_contact'),


]
