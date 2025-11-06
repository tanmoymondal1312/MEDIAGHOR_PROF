# Blog_Posts app - urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('/post-impression/', post_impression, name='post_impression'),
    path('', all_posts, name='all-posts'),
    path('/<str:id>', post, name='post_detail'),

]

