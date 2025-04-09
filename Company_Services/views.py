from django.shortcuts import render
from .models import CompanyService  # Ensure correct import path
from django.shortcuts import get_object_or_404, render



from django.db.models import Q, Case, When, Value, IntegerField

def services(request):
    search = request.GET.get('search', '').strip()
    
    # Get all services ordered by priority by default
    services_datas = CompanyService.objects.all().order_by('-priority')
    
    if search:
        # Split search query into individual words
        search_words = search.split()
        
        # Start with an empty Q object
        q_objects = Q()
        
        # Build a query that checks each word against all fields
        for word in search_words:
            q_objects |= (
                Q(title__icontains=word) |
                Q(short_title__icontains=word) |
                Q(description__icontains=word) |
                Q(explanation__icontains=word)
            )
        
        # Apply the combined query
        services_datas = services_datas.filter(q_objects)
        
        # Annotate with match priority
        services_datas = services_datas.annotate(
            match_priority=Case(
                # Exact match in short_title gets highest priority (4)
                When(short_title__iexact=search, then=Value(4)),
                # All words match in short_title (3)
                When(all_words_match_short_title(search), then=Value(3)),
                # Partial match in short_title (2)
                When(short_title__icontains=search, then=Value(2)),
                # Match in title (1)
                When(title__icontains=search, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-match_priority', '-priority')
    
    context = {
        'services_datas': services_datas,
        'search_query': search,
        'search_performed': bool(search),
    }
    
    return render(request, 'services.html', context)

# Custom function to check if all search words match in short_title
def all_words_match_short_title(search):
    from django.db.models import Q
    search_words = search.split()
    q = Q()
    for word in search_words:
        q &= Q(short_title__icontains=word)
    return q




def service(request,id,contact=None):

    current_post = get_object_or_404(CompanyService, id=id)
    recommended_posts = CompanyService.objects.exclude(id=id).order_by('-priority')[:10]

    print("The Contact Is",contact)

    
    context = {
        'contact':contact,
        'post': current_post,
        'recommended_posts': recommended_posts
    }
    return render(request, 'service.html',context)