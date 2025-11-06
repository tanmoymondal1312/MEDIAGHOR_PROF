from django.urls import path
from .views import *


urlpatterns = [
    path('',AllProducts, name='all_products'),
    path('/dark-screen/',DarkScreenAndroid, name='dark_screen_android'),
    path('/rainbow-tools/',RainbowTools, name='rainbow_tools_home'),
    path('/dark-screen/privacy-policy/',DarkScreenAndroidPrivacyPolicy, name='dark_screen_android_privacy_policy'),
    path('/rainbow-tools/privacy-policy/',RainbowToolsPrivacyPolicy, name='rainbow_android_privay_policy'),
]




