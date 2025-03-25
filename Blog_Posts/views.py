from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import BlogPost

@require_POST
@csrf_exempt  # Remove this if you have CSRF protection set up properly
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