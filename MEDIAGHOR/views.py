from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from Company_Services.models import CompanyService
from Blog_Posts.models import BlogPost
from Resources.models import Library
from django.http import JsonResponse


def home(request):
    search = request.GET.get('search', '').strip()
    per_page = 12
    combined_data = []

    blog_titles = BlogPost.objects.values_list('short_title', flat=True) \
                                 .order_by('-likes') 
    library_titles = Library.objects.values_list('short_title', flat=True) \
                                   .order_by('-copy') 
    short_titles = list(blog_titles) + list(library_titles)

    if not search:
        # Default view - interleave results by priority
        company_services = list(CompanyService.objects.order_by('-priority'))
        blog_posts = list(BlogPost.objects.order_by('-likes'))
        libraries = list(Library.objects.order_by('-copy'))
        
        max_length = max(len(company_services), len(blog_posts), len(libraries))
        
        for i in range(max_length):
            if i < len(blog_posts):
                combined_data.append(blog_posts[i])
            
            if i < len(libraries):
                combined_data.append(libraries[i])
            
            if i < len(company_services):
                combined_data.append(company_services[i])
    else:
        # Search functionality
        # Search in CompanyService
        company_services = CompanyService.objects.filter(
            Q(short_title__icontains=search) | 
            Q(description__icontains=search)
        ).order_by('-priority')
        
        # Search in BlogPost - using correct field names
        blog_posts = BlogPost.objects.filter(
            Q(short_title__icontains=search) | 
            Q(post_content__icontains=search) |
            Q(full_post_content__icontains=search) |
            Q(title__icontains=search)
        ).order_by('-likes')
        
        # Search in Library
        libraries = Library.objects.filter(
            Q(short_title__icontains=search) | 
            Q(description__icontains=search) |
            Q(title__icontains=search)
        ).order_by('-copy')
        
        # Combine all search results with blog posts first
        combined_data = list(blog_posts) + list(libraries) + list(company_services)

    # Pagination
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
        'page_obj': page_obj,
        'search_query': search,
        'short_titles':short_titles
    }

    return render(request, "home.html", context)



def about(request):
    return render(request, "about.html")





def search_suggestions(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', '')
    print("page =======",page)
    
    results = []
    
    if page == 'home':
        # Search in BlogPost
        blog_posts = BlogPost.objects.filter(
            Q(short_title__icontains=query)
        ).order_by('-likes').values('id', 'short_title')[:5]  # Only get needed fields
        
        # Search in Library
        libraries = Library.objects.filter(
            Q(short_title__icontains=query)
        ).order_by('-copy').values('id', 'short_title')[:5]
        
        # Search in CompanyService
        company_services = CompanyService.objects.filter(
            Q(short_title__icontains=query)
        ).order_by('-priority').values('id', 'short_title')[:5]
        results = list(blog_posts) + list(libraries) + list(company_services)

    elif page == 'all_libraries':
        libraries = Library.objects.filter(
            Q(short_title__icontains=query)
        ).order_by('-copy').values('id', 'short_title')[:10]
        results = list(libraries)
    elif page == 'Android_library':
        libraries = Library.objects.filter(
            Q(short_title__icontains=query) &
            Q(category__name="Android")  # Filters by category name
        ).order_by('-copy').values('id', 'short_title')[:10]
        results = list(libraries)
    elif page == 'Django_library':
        libraries = Library.objects.filter(
            Q(short_title__icontains=query) &
            Q(category__name="Django")  # Filters by category name
        ).order_by('-copy').values('id', 'short_title')[:10]
        results = list(libraries)
    elif page == 'Python_library':
        libraries = Library.objects.filter(
            Q(short_title__icontains=query) &
            Q(category__name="Python")  # Filters by category name
        ).order_by('-copy').values('id', 'short_title')[:10]
        results = list(libraries)
   
    elif page == 'services':
        blog_posts = CompanyService.objects.filter(
            Q(short_title__icontains=query)
        ).order_by('-priority').values('id', 'short_title')[:5]  # Only get needed fields
        results = list(blog_posts)

    elif page == 'posts':
        blog_posts = BlogPost.objects.filter(
            Q(short_title__icontains=query)
        ).order_by('-likes').values('id', 'short_title')[:5]  # Only get needed fields
        results = list(blog_posts)



    
    return JsonResponse({'results': results})