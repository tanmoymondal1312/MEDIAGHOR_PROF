from django.shortcuts import render

# Create your views here.

def AllProducts(request):
    return render(request,'all_products.html')

def RainbowTools(request):
    return render(request,'rainbow_android_home.html')

def RainbowToolsPrivacyPolicy(request):
    return render(request,'rainbow_android_privay_policy.html')


def DarkScreenAndroid(request):
    return render(request,'dark_screen_android.html')

def DarkScreenAndroidPrivacyPolicy(request):
    return render(request,'dark_screen_android_privacy_ploicy.html')