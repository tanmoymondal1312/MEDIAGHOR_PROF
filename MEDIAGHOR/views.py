from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from Company_Services.models import CompanyService
from Blog_Posts.models import BlogPost
from Resources.models import Library

def home(request):
    # Get all items from each model, sorted by their respective metrics in descending order
    company_services = list(CompanyService.objects.order_by('-priority'))
    blog_posts = list(BlogPost.objects.order_by('-likes'))
    libraries = list(Library.objects.order_by('-copy'))
    
    # Determine the maximum length among the three lists
    max_length = max(len(company_services), len(blog_posts), len(libraries))
    
    combined_data = []
    
    # Iterate through all possible positions
    for i in range(max_length):
        # Add blog post if available at this position (highest priority first)
        if i < len(blog_posts):
            combined_data.append(blog_posts[i])
        
        # Add library if available at this position
        if i < len(libraries):
            combined_data.append(libraries[i])
        
        # Add company service if available at this position
        if i < len(company_services):
            combined_data.append(company_services[i])
    
    # Pagination
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
        'services_datas': page_obj,
        'count_of_datas': paginator.count,
        'paginator': paginator,
        'page_obj': page_obj
    }

    return render(request, "home.html", context)