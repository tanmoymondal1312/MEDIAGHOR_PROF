from django.shortcuts import render
from .models import Library
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, get_object_or_404
from categories.models import LibraryCategory
from .models import Library
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q





@require_POST
@ensure_csrf_cookie
def click_on_copy(request):
    try:
        # Parse JSON data
        data = json.loads(request.body)
        library_id = data.get('post_id')
        library = Library.objects.get(id=library_id)
        library.copy += 1
        library.save()
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'copies': library.copy,
            'message': 'Copy count updated successfully'
        })
       
    except Library.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

def single_category_resources(request, resourcesName = None):
    # Get the category by slug
    search = request.GET.get('search', '').strip()
    resources_list = None
    category = None



    if resourcesName == None:
        if search:
            resources_list = Library.objects.filter(
                Q(short_title__icontains=search) | 
                Q(description__icontains=search) |
                Q(title__icontains=search)
            ).order_by('-copy')
        else:
            resources_list = Library.objects.all().order_by('-copy')


        paginator = Paginator(resources_list, 10)
        page_number = request.GET.get('page')
        
        try:
            resources = paginator.page(page_number)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)
        page_range = []
        current_page = resources.number
        total_pages = paginator.num_pages
        for num in range(max(1, current_page - 2), min(current_page + 3, total_pages + 1)):
            page_range.append(num)
        
        context = {
            'category': category,
            'services_datas': resources,
            'paginator': paginator,
            'page_range': page_range,
        }
        return render(request, 'all_library.html', context)

    else:
        if search:
            resources_list = Library.objects.filter(
                (Q(short_title__icontains=search) | 
                Q(description__icontains=search) |
                Q(title__icontains=search)) &
                Q(category__slug=resourcesName)
            ).order_by('-copy')
        else:
            category = get_object_or_404(LibraryCategory, slug=resourcesName)
            resources_list = category.libraries.all().order_by('-copy')


        paginator = Paginator(resources_list, 10)
        page_number = request.GET.get('page')
        
        try:
            resources = paginator.page(page_number)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)
        page_range = []
        current_page = resources.number
        total_pages = paginator.num_pages
        for num in range(max(1, current_page - 2), min(current_page + 3, total_pages + 1)):
            page_range.append(num)
        
        context = {
            'category': category,
            'services_datas': resources,
            'paginator': paginator,
            'page_range': page_range,
        }
        return render(request, 'library_by_category.html', context)





    

def library(request,id):

    current_post = get_object_or_404(Library, id=id)

    
    # Get recommended posts using multiple criteria, ordered by likes (descending) and date (descending)
    recommended_posts = Library.objects.filter(
        Q(title__icontains=current_post.short_title) |
        Q(description__icontains=current_post.description)
    ).exclude(id=current_post.id).filter(
        is_for_libraries=True
    ).distinct().order_by('-copy')[:5]  # First by copy, then by date
    
    # Fallback if no recommendations found - get most popular recent posts
    if not recommended_posts.exists():
        recommended_posts = Library.objects.filter(
            is_for_libraries=True
        ).exclude(id=current_post.id).order_by('-copy')[:5]
    
    context = {
        'post': current_post,
        'recommended_posts': recommended_posts
    }
    return render(request, 'library.html',context)