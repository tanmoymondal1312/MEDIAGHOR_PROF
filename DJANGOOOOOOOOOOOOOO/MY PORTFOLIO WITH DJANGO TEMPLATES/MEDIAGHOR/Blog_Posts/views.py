from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .models import BlogPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q



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
    search = request.GET.get('search', '').strip()

    if(not search):
        posts_list = BlogPost.objects.all().order_by('-likes')
    else:
        posts_list = BlogPost.objects.filter(
            Q(short_title__icontains=search) | 
            Q(post_content__icontains=search) |
            Q(full_post_content__icontains=search) |
            Q(title__icontains=search)
        ).order_by('-likes')



    # Paginate with 12 items per page
    paginator = Paginator(posts_list, 12)
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


def post(request,id):

    current_post = get_object_or_404(BlogPost, id=id)
    
    current_post.views+=1
    current_post.save()

    
    # Get recommended posts using multiple criteria, ordered by likes (descending) and date (descending)
    recommended_posts = BlogPost.objects.filter(
        Q(title__icontains=current_post.short_title) |
        Q(post_content__icontains=current_post.short_title) |
        Q(full_post_content__icontains=current_post.short_title)
    ).exclude(id=current_post.id).filter(
        is_for_blog_posts=True
    ).distinct().order_by('-likes', '-created_at')[:5]  # First by likes, then by date
    
    # Fallback if no recommendations found - get most popular recent posts
    if not recommended_posts.exists():
        recommended_posts = BlogPost.objects.filter(
            is_for_blog_posts=True
        ).exclude(id=current_post.id).order_by('-likes', '-created_at')[:5]
    
    context = {
        'post': current_post,
        'recommended_posts': recommended_posts
    }
    return render(request, 'post.html',context)