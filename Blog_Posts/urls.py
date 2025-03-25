from django.urls import path
from .views import post_impression  # Import the view we created

urlpatterns = [
    path('post-impression/', post_impression, name='post_impression'),
    # Add other blog URLs as needed...
]