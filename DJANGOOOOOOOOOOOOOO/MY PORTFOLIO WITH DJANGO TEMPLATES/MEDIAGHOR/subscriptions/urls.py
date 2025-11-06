from django.urls import path
from .views import *


urlpatterns = [
    path('',subscribe_view,name="subscribe"),
    path('/api-contact',ContactView,name="contact"),

]



