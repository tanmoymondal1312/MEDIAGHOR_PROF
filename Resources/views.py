from django.shortcuts import render
from models import Library
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


# Create your views here.




@require_POST
def click_on_coppy(request):
    try:
        # Parse JSON data
        data = json.loads(request.body)
        library_id = data.get('post_id')
        
            
        library = Library.objects.get(id=library_id)
        library.coppy+=1
        library.save()
       
    except Library.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Server error'}, status=500)