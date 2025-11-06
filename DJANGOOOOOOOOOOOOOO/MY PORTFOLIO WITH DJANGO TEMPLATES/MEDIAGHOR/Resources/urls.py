from django.urls import path
from .views import click_on_copy,single_category_resources,library,RequestResourcesPage,contribute_for_resources,submit_contribution,request_for_resources,contribution_success


urlpatterns = [
    path('/click_on_copy/', click_on_copy, name='click_on_copy'),
    path('', single_category_resources, name='category_resources'),
    path('/category=<slug:resourcesName>', single_category_resources, name='single_category_resources'),
    path('/<str:id>', library, name='library_detail'),
    path('/request-resources/', RequestResourcesPage, name='request_resources_page'),
    path('api/request-for-resources/', request_for_resources, name='request_for_resources'),
    
    
    
    path('/contribute/', contribute_for_resources, name='contribute_for_resources'),
    path('/contribute/submit/', submit_contribution, name='submit_contribution'),
    path('/contribute/success/', contribution_success, name='contribution_success'),
    # path('api/categories/', views.get_categories_json, name='get_categories_json'),
    # path('api/validate-title/', views.validate_resource_title, name='validate_resource_title'),


    # Add other blog URLs as needed...
]