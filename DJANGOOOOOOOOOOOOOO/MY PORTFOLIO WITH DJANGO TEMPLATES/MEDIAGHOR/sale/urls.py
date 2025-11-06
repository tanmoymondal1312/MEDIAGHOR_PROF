from django.urls import path
from .views import *


urlpatterns = [
    path('/rainbow-tools',RainbowToolsSale, name='rainbow_android_sale'),
    
]




