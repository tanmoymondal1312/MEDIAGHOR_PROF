from django.urls import path
from .views import post_impression,all_posts  # Import the view we created

urlpatterns = [
    path('post-impression/', post_impression, name='post_impression'),
    path('all-posts/', all_posts, name='all-posts'),

    # Add other blog URLs as needed...
]