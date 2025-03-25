import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from Company_Services.models import CompanyService
from Blog_Posts.models import BlogPost
from Resources.models import Library

def home(request):
    datas_of_company_service = list(CompanyService.objects.all())  
    datas_of_blog_post = list(BlogPost.objects.all())
    datas_of_libraries = list(Library.objects.all())

    # Combine and shuffle data
    combined_data = datas_of_company_service + datas_of_blog_post + datas_of_libraries
    random.shuffle(combined_data)
    
    # Pagination setup
    per_page = 12
    paginator = Paginator(combined_data, per_page)
    page = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'services_datas': page_obj,  # This will now contain only paginated data
        'count_of_datas': paginator.count,  # Total count of data
        'paginator': paginator,  # Paginator object
        'page_obj': page_obj  # Current page object
    }

    return render(request, "home.html", context)




