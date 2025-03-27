from django.shortcuts import render
from .models import Library
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, get_object_or_404
from categories.models import LibraryCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




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
    

def single_category_resources(request, resourcesName):
    # Get the category by slug
    category = get_object_or_404(LibraryCategory, slug=resourcesName)
    
    # Get all resources in this category, ordered by copies (highest first)
    resources_list = category.libraries.all().order_by('-copy')
    
    # Paginate with 12 items per page
    paginator = Paginator(resources_list, 1)
    page_number = request.GET.get('page')
    
    try:
        resources = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        resources = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        resources = paginator.page(paginator.num_pages)
    
    # Calculate page range for limited numbered links (e.g., show only nearby pages)
    page_range = []
    current_page = resources.number
    total_pages = paginator.num_pages
    
    # Show 2 pages before and after current page
    for num in range(max(1, current_page - 2), min(current_page + 3, total_pages + 1)):
        page_range.append(num)
    
    context = {
        'category': category,
        'services_datas': resources,
        'paginator': paginator,
        'page_range': page_range,  # For limited numbered pagination
    }
    
    return render(request, 'library_by_category.html', context)