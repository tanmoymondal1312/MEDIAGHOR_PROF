from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q

import json
import threading
import uuid

from .models import Library, LibraryCategory, ResourcesPublisher, ResourceRequest
from categories.models import LibraryCategory







@require_POST
@ensure_csrf_cookie
def click_on_copy(request):
    try:
        # Parse JSON data
        data = json.loads(request.body)

        library_id = data.get('post_id')

        library = Library.objects.get(id=library_id)

        # Increment copy count
        library.copy += 1
        library.save()

        # Return success response
        response = {
            'status': 'success',
            'copies': library.copy,
            'message': 'Copy count updated successfully'
        }
        print("🔹 Sending response:", response)
        return JsonResponse(response)

    except Library.DoesNotExist:
        print("❌ Library.DoesNotExist: No post found with id", library_id)
        return JsonResponse({'status': 'error', 'message': 'Post not found'}, status=404)

    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", str(e))
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

def single_category_resources(request, resourcesName=None):
    search = request.GET.get('search', '').strip()
    resources_list = None
    category = None
    is_all_resources = False

    try:
        if resourcesName is None:
            # All resources
            is_all_resources = True
            if search:
                resources_list = Library.objects.filter(
                    Q(short_title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(title__icontains=search),
                    is_active=True
                ).order_by('-copy')
            else:
                resources_list = Library.objects.filter(is_active=True).order_by('-copy')

        else:
            # Specific category
            category_slug = resourcesName.strip()
            category = get_object_or_404(LibraryCategory, slug=category_slug)

            if search:
                resources_list = Library.objects.filter(
                    (Q(short_title__icontains=search) |
                     Q(description__icontains=search) |
                     Q(title__icontains=search)) &
                    Q(category__slug=category_slug),
                    is_active=True
                ).order_by('-copy')
            else:
                resources_list = category.libraries.filter(is_active=True).order_by('-copy')

        # Pagination
        paginator = Paginator(resources_list, 10)
        page_number = request.GET.get('page')

        try:
            resources = paginator.page(page_number)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)

        current_page = resources.number
        total_pages = paginator.num_pages
        page_range = list(range(max(1, current_page - 2), min(total_pages + 1, current_page + 3)))

        context = {
            'category': category,
            'services_datas': resources,
            'paginator': paginator,
            'page_range': page_range,
            'search': search,
            'is_all_resources': is_all_resources,
        }

        return render(request, 'library_by_category.html', context)

    except Http404:
        context = {'category': None, 'services_datas': [], 'paginator': None, 'page_range': [], 'search': search,
                   'is_all_resources': False, 'error_message': f"Category '{resourcesName}' not found."}
        return render(request, 'library_by_category.html', context, status=404)
    except Exception as e:
        context = {'category': None, 'services_datas': [], 'paginator': None, 'page_range': [], 'search': search,
                   'is_all_resources': False, 'error_message': "An error occurred while loading resources."}
        return render(request, 'library_by_category.html', context, status=500)


    

def library(request,id):

    current_post = get_object_or_404(Library, id=id)
    current_post.views += 1
    current_post.save()

    
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

def RequestResourcesPage(request):
    """
    View for rendering the request resources page
    """
    # Get all categories for the dropdown
    categories = LibraryCategory.objects.all().order_by('name')
    
    context = {
        'categories': categories,
        'page_title': 'Request Resources - Media Ghor',
        'meta_description': 'Request custom programming resources, libraries, and tools from Media Ghor. Get free coding resources tailored to your development needs.',
    }
    
    return render(request, 'request_resources.html', context)

@require_http_methods(["POST"])
@csrf_exempt
def request_for_resources(request):
    """
    API endpoint to handle resource request submissions
    """
    if request.method == 'POST':
        try:
            # Get form data
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            resource_title = request.POST.get('resource_title', '').strip()
            resource_category_slug = request.POST.get('resource_category', '').strip()
            resource_description = request.POST.get('resource_description', '').strip()
            urgency = request.POST.get('urgency', 'medium')
            
            # Basic validation
            if not all([full_name, email, resource_title, resource_category_slug, resource_description]):
                return JsonResponse({
                    'success': False,
                    'message': 'All required fields must be filled out.'
                }, status=400)
            
            # Validate email format
            if '@' not in email or '.' not in email:
                return JsonResponse({
                    'success': False,
                    'message': 'Please provide a valid email address.'
                }, status=400)
            
            # Get category object
            try:
                category = LibraryCategory.objects.get(slug=resource_category_slug)
            except LibraryCategory.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid category selected.'
                }, status=400)
            
            # Create resource request
            resource_request = ResourceRequest(
                full_name=full_name,
                email=email,
                resource_title=resource_title,
                category=category,
                resource_description=resource_description,
                urgency=urgency,
                status='pending'
            )
            
            resource_request.save()
            
            # Send notification to admin only (optional - if it fails, no action needed)
            try:
                send_admin_notification(resource_request)
            except Exception as email_error:
                # Just log the email error but don't affect the main functionality
                print(f"Email notification failed (non-critical): {str(email_error)}")
                # Continue with the successful response
            
            return JsonResponse({
                'success': True,
                'message': 'Your resource request has been submitted successfully! We will review it and get back to you soon.',
                'request_id': resource_request.id
            })
            
        except Exception as e:
            # Log the error for debugging
            print(f"Error processing resource request: {str(e)}")
            
            return JsonResponse({
                'success': False,
                'message': 'An error occurred while processing your request. Please try again later.'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)

def send_admin_notification(resource_request):
    """
    Send notification email to admin about new resource request (async).
    """

    def _send():
        try:
            subject = f"New Resource Request: {resource_request.resource_title}"

            message = f"""
            New Resource Request Received:

            Request Details:
            ---------------
            Name: {resource_request.full_name}
            Email: {resource_request.email}
            Resource Title: {resource_request.resource_title}
            Category: {resource_request.category.name}
            Urgency: {resource_request.get_urgency_display()}
            Date: {resource_request.created_at.strftime("%B %d, %Y at %H:%M")}
            Request ID: #{resource_request.id}

            Description:
            ------------
            {resource_request.resource_description}

            Please review this request in the admin panel.
            """

            admin_email = getattr(settings, 'ADMIN_EMAIL', 'tanmoymondal1315@gmail.com')

            send_mail(
                subject=subject,
                message=message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_email],
                fail_silently=False,
            )

            print(f"✅ Admin notification sent for request ID {resource_request.id}")

        except Exception as e:
            print(f"❌ Error sending admin notification: {str(e)}")

    # Start background thread
    threading.Thread(target=_send).start()
    
    



def submission_notify_to_admin(publisher, library):
    """
    Send notification email to admin about new resource submission (async).
    """
    def _send():
        try:
            subject = f"New Resource Submitted: {library.id}"
            message = f"""
            Library Details:
            ---------------
            Request ID: #{library.id}
            Author Name: {publisher.name}
            Author Email: {publisher.email}
            Resource Title: {library.title}
            Short Description: {library.short_title}
            Category: {library.category.name}

            Description:
            ------------
            {library.description}

            Please review this request in the admin panel.
            """

            send_mail(
                subject=subject,
                message=message.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["tanmoymondal1315@gmail.com"],
                fail_silently=False,
            )

            print(f"✅ Admin email sent for resource {library.id}")

        except Exception as e:
            print(f"❌ Error sending admin notification: {str(e)}")

    # Start async thread
    threading.Thread(target=_send).start()



def submission_notify_to_publisher(publisher_email, library):
    """
    Send a confirmation email to the publisher (async).
    """
    def _send():
        try:
            subject = "🎉 Thank You for Publishing Your Resource!"
            text_content = f"""
            Thank you for publishing your resource titled "{library.title}".
            We will review it within 24 hours.
            """

            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f9fafc; color: #333; padding: 30px;">
                <div style="max-width: 600px; margin: auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
                    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); color: white; padding: 20px; text-align: center;">
                        <h2 style="margin: 0;">Thank You for Sharing Your Resource!</h2>
                    </div>
                    <div style="padding: 25px;">
                        <p style="font-size: 16px;">Hi there 👋,</p>
                        <p style="font-size: 16px;">We’ve received your submission:</p>
                        <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 15px 0;">
                            <p style="margin: 0; font-size: 15px;">
                                <strong>📘 Title:</strong> {library.title}<br>
                                <strong>🆔 Resource ID:</strong> {library.id}<br>
                                <strong>📂 Category:</strong> {library.category.name if library.category else "Uncategorized"}
                            </p>
                        </div>
                        <p style="font-size: 15px;">
                            Our team will review your resource within <strong>24 hours</strong>.
                            You’ll receive another email once it’s approved and published.
                        </p>
                        <p style="font-size: 15px;">Thank you for contributing to our platform and helping others learn! 🙌</p>
                        <hr style="border: none; border-top: 1px solid #eee; margin: 25px 0;">
                        <p style="font-size: 13px; color: #777; text-align: center;">
                            — The Mediaghor Team<br>
                            <a href="https://mediaghor.com" style="color: #4f46e5; text-decoration: none;">Visit Website</a>
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[publisher_email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            print(f"✅ Publisher email sent to {publisher_email}")

        except Exception as e:
            print(f"❌ Error sending publisher notification: {str(e)}")

    # Start async thread
    threading.Thread(target=_send).start()

    
    
    
    
    
    
    
    
def contribute_for_resources(request):
    """
    View for the resource contribution page
    """
    # Get all categories for the dropdown
    categories = LibraryCategory.objects.filter().order_by('name')
    
    context = {
        'categories': categories,
        'title': 'Contribute Resources - Media Ghor',
        'meta_description': 'Share your programming resources, libraries, and tools with the Media Ghor developer community. Contribute to help developers worldwide.',
    }
    print("Hello in contribute")
    
    return render(request, 'contribute_for_resources.html', context)



@csrf_protect
@require_http_methods(["POST"])
def submit_contribution(request):
    """
    Handle form submission for resource contributions
    """
    print("Sunmit Called")
    if request.method == 'POST':
        print("Request Post")

        try:
            # Get form data
            
            name = request.POST.get('contributor_name','').strip()
            email = request.POST.get('contributor_email','').strip()
            number = request.POST.get('contributor_phone','').strip()
            
            print(name,email,number)
            
            title = request.POST.get('title', '').strip()
            short_title = request.POST.get('short_title', '').strip()
            description = request.POST.get('description', '').strip()
            library_link = request.POST.get('library_link', '').strip()
            how_to_use = request.POST.get('how_to_use', '').strip()
            category_id = request.POST.get('category')
            
            
            
            
            # Basic validation
            if not all([name,email,number,title, short_title, description, library_link, category_id]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('resources:contribute_for_resources')
            
            # Validate field lengths
            if len(title) > 255:
                messages.error(request, 'Title is too long. Maximum 255 characters allowed.')
                return redirect('resources:contribute_for_resources')
            
            if len(short_title) > 50:
                messages.error(request, 'Short title is too long. Maximum 50 characters allowed.')
                return redirect('resources:contribute_for_resources')
            
            if len(library_link) > 500:
                messages.error(request, 'Resource link is too long. Maximum 500 characters allowed.')
                return redirect('resources:contribute_for_resources')
            
            # Get category instance
            try:
                category = LibraryCategory.objects.get(id=category_id)
            except LibraryCategory.DoesNotExist:
                messages.error(request, 'Selected category is not valid.')
                return redirect('resources:contribute_for_resources')
            
            # Generate unique ID for the library
            base_slug = slugify(short_title or title[:30])
            library_id = f"{base_slug}-{str(uuid.uuid4())[:8]}"
            
            #Create Library Author
            publisher = ResourcesPublisher(
                name = name,
                email = email,
                number = number
            )
            publisher.save()
            # Create the library instance
            library = Library(
                is_active = False,
                id=library_id,
                title=title,
                short_title=short_title,
                description=description,
                library_link=library_link,
                how_to_use=how_to_use,
                category=category,
                is_for_libraries=True,  # Default to True for contributions
                copy=0,  # Initialize copy count
                views=0,   # Initialize view count
                publisher = publisher
            )
            
            # Save the instance
            library.save()
            
            
            try:
                submission_notify_to_admin(publisher,library)
            except Exception as email_error:
                # Just log the email error but don't affect the main functionality
                print(f"Email notification failed (non-critical): {str(email_error)}")
                # Continue with the successful response
                
            try:
                submission_notify_to_publisher(publisher.email,library)
            except Exception as email_error:
                # Just log the email error but don't affect the main functionality
                print(f"Email notification failed (non-critical): {str(email_error)}")
                # Continue with the successful response
            
            # Success message
            messages.success(
                request, 
                'Thank you for your contribution! Your resource has been submitted for review. '
                'We will notify you once it\'s published.'
            )
            
            # Redirect to success page or back to contribute page
            return redirect('resources:contribution_success')
            
        except IntegrityError:
            messages.error(
                request, 
                'A resource with similar details already exists. Please check your submission.'
            )
            return redirect('resources:contribute_for_resources')
            
        except Exception as e:
            # Log the error for debugging
            print(f"Error submitting contribution: {str(e)}")
            messages.error(
                request, 
                'An error occurred while submitting your contribution. Please try again later.'
            )
            return redirect('resources:contribute_for_resources')
    
    # If not POST, redirect to contribute page
    return redirect('resources:contribute_for_resources')

def contribution_success(request):
    """
    Success page after contribution submission
    """
    context = {
        'title': 'Contribution Submitted - Media Ghor',
        'meta_description': 'Thank you for contributing to Media Ghor. Your resource has been submitted for review.',
    }
    return render(request, 'contribution_success.html', context)

# def get_categories_json(request):
#     """
#     API endpoint to get categories as JSON (for potential AJAX use)
#     """
#     categories = LibraryCategory.objects.filter().order_by('name')
#     categories_data = [
#         {
#             'id': cat.id,
#             'name': cat.name,
#             'slug': cat.slug,
#             'description': cat.description
#         }
#         for cat in categories
#     ]
#     return JsonResponse({'categories': categories_data})

# @csrf_protect
# def validate_resource_title(request):
#     """
#     AJAX endpoint to validate if a resource title already exists
#     """
#     if request.method == 'POST':
#         title = request.POST.get('title', '').strip()
#         short_title = request.POST.get('short_title', '').strip()
        
#         response_data = {
#             'title_valid': True,
#             'short_title_valid': True,
#             'suggestions': []
#         }
        
#         # Check if title exists
#         if title:
#             existing_titles = Library.objects.filter(
#                 title__iexact=title
#             ).exists()
#             if existing_titles:
#                 response_data['title_valid'] = False
        
#         # Check if short title exists
#         if short_title:
#             existing_short_titles = Library.objects.filter(
#                 short_title__iexact=short_title
#             ).exists()
#             if existing_short_titles:
#                 response_data['short_title_valid'] = False
#                 # Generate suggestions
#                 base_slug = slugify(short_title)
#                 suggestions = [
#                     f"{short_title}-lib",
#                     f"{short_title}-tool",
#                     f"{short_title}-{str(uuid.uuid4())[:4]}"
#                 ]
#                 response_data['suggestions'] = suggestions
        
#         return JsonResponse(response_data)
    
#     return JsonResponse({'error': 'Invalid request method'})

# # Optional: Admin view to see pending contributions

