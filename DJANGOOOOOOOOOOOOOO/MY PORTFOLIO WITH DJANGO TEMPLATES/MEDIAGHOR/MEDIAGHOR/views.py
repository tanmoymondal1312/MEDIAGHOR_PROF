from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from Company_Services.models import CompanyService
from Blog_Posts.models import BlogPost
from Resources.models import Library
from django.http import JsonResponse
from categories.models import LibraryCategory



def home(request):
    search = request.GET.get('search', '').strip()
    per_page = 12
    combined_data = []

    # Get short titles for suggestions/autocomplete
    blog_titles = BlogPost.objects.values_list('short_title', flat=True).order_by('-likes')
    library_titles = Library.objects.filter(is_active=True).values_list('short_title', flat=True).order_by('-copy')
    short_titles = list(blog_titles) + list(library_titles)

    if not search:
        # Default view - interleave blog posts and active libraries
        blog_posts = list(BlogPost.objects.order_by('-likes'))
        libraries = list(Library.objects.filter(is_active=True).order_by('-copy'))
        
        max_length = max(len(blog_posts), len(libraries))
        
        for i in range(max_length):
            if i < len(blog_posts):
                combined_data.append(blog_posts[i])
            if i < len(libraries):
                combined_data.append(libraries[i])
    else:
        # Search view
        blog_posts = BlogPost.objects.filter(
            Q(short_title__icontains=search) |
            Q(post_content__icontains=search) |
            Q(full_post_content__icontains=search) |
            Q(title__icontains=search)
        ).order_by('-likes')

        libraries = Library.objects.filter(
            Q(short_title__icontains=search) |
            Q(description__icontains=search) |
            Q(title__icontains=search),
            is_active=True
        ).order_by('-copy')

        # Combine search results
        combined_data = list(blog_posts) + list(libraries)

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
        'short_titles': short_titles,
    }

    return render(request, "home.html", context)


def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")





def search_suggestions(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', '')
    print("page =======",page)
    print("query=======",query)
    
    results = []
    
    if page == 'home':
        # Search in BlogPost
        blog_posts = BlogPost.objects.filter(
            Q(short_title__icontains=query)
        ).order_by('-likes').values('id', 'short_title')[:5]  # Only get needed fields
        
        # Search in Library
        libraries = Library.objects.filter(
            Q(short_title__icontains=query),
            is_active=True

        ).order_by('-copy').values('id', 'short_title')[:5]
        
        # Search in CompanyService
        company_services = CompanyService.objects.filter(
            Q(short_title__icontains=query)
        ).order_by('-priority').values('id', 'short_title')[:5]
        results = list(blog_posts) + list(libraries) + list(company_services)

    

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
        
    else:
        if page == 'all':
            libraries = Library.objects.filter(
                Q(short_title__icontains=query),
                 is_active=True

            ).order_by('-copy').values('id', 'short_title')[:10]
            results = list(libraries)
        else:
            try:
                # Check if page corresponds to a valid category
                category = LibraryCategory.objects.get(slug=page)
                libraries = Library.objects.filter(
                    Q(short_title__icontains=query) &
                    Q(category=category),
                    is_active=True

                ).order_by('-copy').values('id', 'short_title')[:10]
                results = list(libraries)
            except LibraryCategory.DoesNotExist:
                # Handle case where page is not a valid category slug
                results = []



    
    return JsonResponse({'results': results})












