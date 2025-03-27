from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .models import BlogPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@require_POST
@ensure_csrf_cookie 
def post_impression(request):
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        action = data.get('action')
        
        if not post_id or action not in ['like', 'unlike']:
            return JsonResponse({'success': False, 'error': 'Invalid parameters'})

        try:
            post = BlogPost.objects.get(id=post_id)
            
            if action == 'like':
                post.likes += 1
            elif action == 'unlike':
                post.likes = max(0, post.likes - 1)
            
            post.save()
            
            return JsonResponse({
                'success': True,
                'new_likes': post.likes,
                'action': action
            })

        except BlogPost.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    




def all_posts(request):
    # Get all posts ordered by likes (highest first)
    posts_list = BlogPost.objects.all().order_by('-likes')
    
    # Paginate with 12 items per page
    paginator = Paginator(posts_list, 4)
    page_number = request.GET.get('page')
    
    try:
        services_datas = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        services_datas = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        services_datas = paginator.page(paginator.num_pages)
    
    # Calculate page range for numbered links (show 2 pages before/after current)
    current_page = services_datas.number
    page_range = []
    for num in range(max(1, current_page - 2), min(current_page + 3, paginator.num_pages + 1)):
        page_range.append(num)
    
    context = {
        'services_datas': services_datas,  # Using your required key name
        'paginator': paginator,
        'page_range': page_range,
    }
    
    return render(request, 'all_posts.html', context)